import json
import logging
import datetime
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for
from data.data import DataManager
from utils.db_manager import OrderDBManager, ProductDBManager, UserDBManager
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.user import User
from data.user_manager import UserManager
from data.product_manager import ProductManager
from data.order_manager import OrderManager



logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('app')

app = Flask(__name__)
app.secret_key = "82dhgf68h5d2d250fs5gd40f"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

cors = CORS(app)

OrderDBManager.create_table_orders()
ProductDBManager.create_table_products()
ProductDBManager.create_table_available()
UserDBManager.create_table_user()

def admin_level_required(func):
    def secure_func():
        if current_user.level > 0:
            return redirect(url_for("login"))
        return func

    return secure_func

@login_manager.user_loader
def load_user(user_id):
    return UserManager.get_user(user_id=user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserManager.get_user(email=email)
        next = request.args.get('next')

        if user and (user.password == password):
            login_user(user)

            flash('Logged in successfully.')
            print(f"username: {user.email} auth: {user.is_authenticated}")

            print(f"next: {next}")

            return redirect(next or url_for('home'))
        else:
            return redirect(url_for('login', next=next, error=True))
            

    return render_template('login.html')

@app.route('/check-logged-in')
def check_logged_in():
    return {"logged_in": current_user.is_authenticated}

@app.route('/test-login', methods=['GET', 'POST'])
def test_login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserManager.get_user(email=email)
        next = request.args.get('next')

        if user and (user.password == password):
            login_user(user)

            flash('Logged in successfully.')
            print(f"username: {user.email} auth: {user.is_authenticated}")

            print(f"next: {next}")

            return "ok", 200
        else:
            return "Usuário ou senha incorretos", 401
            

    return render_template('login.html')

# registar antigo, ver novo: registrar2
@app.route('/registrar', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        
        if UserManager.get_user(email=email):
            return redirect(url_for('registrar', email_error=True))
        elif password != confirm_password:
            return redirect(url_for('registrar', pass_error=True))
        else:
            UserManager.add_user(email, name, 1, password)
            return redirect('/login')

    return render_template('registrar.html')

@app.route('/registrar2', methods=['GET', 'POST'])
def register2():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not (email and name and password and confirm_password):
            return "Todos os campos são obrigatórios", 401
        elif password != confirm_password:
            return "As duas senhas inseridas são diferentes", 401
        elif UserManager.get_user(email=email):
            return "Email já cadastrado.", 401
        else:
            UserManager.add_user(email, name, 1, password)
            return "Registrado", 200

    return render_template('registrar.html')

@app.route('/logout')
@login_required
def logout():
    logger.debug(f"User {current_user.name} logging out")
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/painel')
@login_required
def admin_panel():
    return render_template('admin-panel.html')

@app.route('/pedido/novo')
@login_required
def new_order_page():

    return render_template('list_page.html')


@app.route('/pedido/get-list')
@login_required
def get_today_list():
    products_list = ProductManager.get_available_products()
    products_dicts = [product.to_dict() for product in products_list]

    return json.dumps(products_dicts, ensure_ascii=False).encode('utf8')


# @app.route('/save-order', methods=['POST'])
def save_order():
    order = request.get_json()['order']
    DataManager.save_order(order)

    return "1"


@app.route('/save-order', methods=['POST'])
def save_order_db():
    order = request.get_json()['order']
   
    date = int(datetime.datetime.now().timestamp()*1000)
    items = order['items']
    total = order['total']

    OrderManager.save_order(int(current_user.get_id()), date, items, total, 0)
    
    return "1"


@app.route('/historico')
@login_required
def orders_history():
    return render_template("orders_page.html")


@app.route('/get-all-orders')
def get_all_orders():
    orders = OrderManager.get_orders(user_id=int(current_user.get_id()))
    orders_dicts = [order.to_dict() for order in orders]
    
    return json.dumps(orders_dicts, ensure_ascii=False).encode('utf8')


@app.route('/get_orders/by_id/<int:order_id>')
def get_orders_filter(order_id):
    order = OrderManager.get_order_by_id(int(current_user.get_id()), order_id)
    order_dict = order.to_dict()

    return json.dumps(order_dict, ensure_ascii=False).encode('utf8')


@app.route('/get_orders/by_date/<int:time_from>+<int:time_to>')
def get_orders_by_date(time_from, time_to):
    
    orders = OrderManager.get_orders_by_date(user_id=int(current_user.get_id()), time_from=time_from, time_to=time_to)
    orders_dicts = [order.to_dict() for order in orders]

    return json.dumps(orders_dicts, ensure_ascii=False).encode('utf8')

@app.route('/admin_get_orders/by_date/<int:time_from>+<int:time_to>')
def get_orders_admin(time_from, time_to):
    orders = OrderManager.get_orders(time_from=time_from, time_to=time_to)
    orders_dicts = [order.to_dict() for order in orders]

    return json.dumps(orders_dicts, ensure_ascii=False).encode('utf8')


@app.route('/admin_get_orders/filter/')
def get_orders_filter_admin():
    time_from = request.args.get("time_from")
    time_to = request.args.get("time_to")
    name = request.args.get("name")
    order_id = request.args.get("num")

    orders = OrderManager.get_orders(user_name=name, order_id=order_id, time_from=time_from, time_to=time_to)
    orders_dicts = [order.to_dict() for order in orders]

    return json.dumps(orders_dicts, ensure_ascii= False).encode('utf8')


@app.route('/admin_get_orders_today')
def get_orders_today():
    today = datetime.date.today()
    midnight = datetime.datetime.combine(today, datetime.datetime.min.time())
    time_from = int(midnight.timestamp()) * 1000
    day_in_millis = 86400000
    time_to = time_from + day_in_millis

    orders = OrderManager.get_orders(time_from=time_from, time_to=time_to)
    orders_dicts = [order.to_dict() for order in orders]

    return json.dumps(orders_dicts, ensure_ascii=False).encode('utf8')

@app.route('/set-available', methods=['POST'])
def set_available_products():
    ProductManager.delete_all_available_products()
    items = request.get_json()['items']
    for item in items:
        ProductManager.add_available_product(id=item['id'], price=item['price'])
    
    return "OK", 201

@app.route('/get-all-products')
def get_all_products():
    products = ProductManager.get_all_products()
    products_dict_list = [product.to_dict() for product in products]
    return json.dumps(products_dict_list, ensure_ascii=False).encode('utf8')

@app.route('/get-all-products-full')
def get_all_products_full():
    products = ProductManager.get_all_products_full()
    products_dict_list = [product.to_dict() for product in products]
    return json.dumps(products_dict_list, ensure_ascii=False).encode('utf8')

@app.route('/verify-order', methods=['POST'])
def verify_order():
    """
    receives post request-
    post data:
    'order':{'item':str, 'quant':float}
    'cookies': cookies data
    'user': str
    """

    order = request.get_json()
    print(order)
    pre_saved = 'UserData.pre_save_order(order)'

    return pre_saved

@app.route('/x')
def test_populate_products():
    products = [{"name": "Morango", "category": 1, "unit": "CX"},
                {"name": "Chuchu", "category": 1, "unit": "CX"},
                {"name": "Chicória", "category": 1, "unit": "UN"},
                {"name": "Abóbora", "category": 1, "unit": "CX"},
                {"name": "Manga", "category": 1, "unit": "CX"},
                {"name": "Uva", "category": 1, "unit": "UN"},
                {"name": "Espinafre", "category": 1, "unit": "UN"},
                {"name": "Poncan", "category": 1, "unit": "CX"},
                {"name": "Vagem", "category": 1, "unit": "CX"},
                {"name": "Jiló", "category": 1, "unit": "CX"},
                {"name": "Repolho", "category": 1, "unit": "CX"},
                {"name": "Milho", "category": 1, "unit": "CX"}]

    for product in products:
        ProductDBManager.add_product(**product)


def test_get_products():
    products = ProductDBManager.get_all_products()
 
    for product in products:
        print(json.dumps(product) + "\n")

    return json.dumps(products, ensure_ascii=False).encode('utf8')


def test_populate_available():
    ProductDBManager.add_avilable_product(1, 20.0)
    ProductDBManager.add_avilable_product(2, 35.0)
    ProductDBManager.add_avilable_product(3, 27.5)
    ProductDBManager.add_avilable_product(4, 33.0)
    ProductDBManager.add_avilable_product(5, 19.0)
    ProductDBManager.add_avilable_product(6, 2.2)
    ProductDBManager.add_avilable_product(7, 3.0)
    ProductDBManager.add_avilable_product(8, 50.0)
    ProductDBManager.add_avilable_product(9, 30.0)
    ProductDBManager.add_avilable_product(10, 1.5)
    ProductDBManager.add_avilable_product(11, 42.0)

    print(ProductDBManager.get_available_products())


def test_users():
    UserDBManager.create_table_user()

    return json.dumps(UserDBManager.get_user(1))

@app.route('/test', methods=["POST"])
def test1():
    data = request.form
    print(data)

    return "failed", 401
    


@app.route('/x')
def test():
    return f"{int(datetime.datetime.now().timestamp()*1000)}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    


