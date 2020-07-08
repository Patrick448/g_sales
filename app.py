import json
import logging
from flask import Flask, request, render_template
from data.data import DataManager
from utils.db_manager import OrderDBManager, ProductDBManager, UserDBManager

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('app')

app = Flask(__name__)

OrderDBManager.create_table_orders()
ProductDBManager.create_table_products()
ProductDBManager.create_table_available()

for order in OrderDBManager.get_all_orders_by_user(user_id="001"):
    print(order)


@app.route('/')
def home():
    return render_template('list_page.html')


@app.route('/pedido/novo')
def new_order_page():

    return render_template('list_page.html')


@app.route('/pedido/get-list')
def get_today_list():

    return json.dumps(ProductDBManager.get_available_products(), ensure_ascii=False).encode('utf8')


# @app.route('/save-order', methods=['POST'])
def save_order():
    order = request.get_json()['order']
    DataManager.save_order(order)

    return "1"


@app.route('/save-order', methods=['POST'])
def save_order_db():
    order = request.get_json()['order']
    OrderDBManager.save_order("001", order)

    return "1"


@app.route('/historico')
def orders_history():
    return render_template("orders_page.html")


@app.route('/get-all-orders')
def get_all_orders():

    return json.dumps(OrderDBManager.get_all_orders())


@app.route('/get_orders/by_id/<int:order_id>')
def get_orders_filter(order_id):
    db_response = OrderDBManager.get_order_by_id("001", order_id)
    return json.dumps(db_response)


@app.route('/get_orders/by_date/<int:time_from>+<int:time_to>')
def get_orders_by_date(time_from, time_to):
    db_response = OrderDBManager.get_order_by_date(user_id="001", time_from=time_from, time_to=time_to)
    return json.dumps(db_response)


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


def test_populate_products():
    products = [{"name": "Banana", "category": 1, "unit": "CX"},
                {"name": "Maçã", "category": 1, "unit": "CX"},
                {"name": "Melancia", "category": 1, "unit": "UN"},
                {"name": "Batata", "category": 1, "unit": "CX"},
                {"name": "Cenoura", "category": 1, "unit": "CX"},
                {"name": "Alface", "category": 1, "unit": "UN"},
                {"name": "Agrião", "category": 1, "unit": "UN"},
                {"name": "Tomate", "category": 1, "unit": "CX"},
                {"name": "Laranja", "category": 1, "unit": "CX"},
                {"name": "Inhame", "category": 1, "unit": "CX"},
                {"name": "Couve", "category": 1, "unit": "CX"},
                {"name": "Beterraba", "category": 1, "unit": "CX"}]

    for product in products:
        ProductDBManager.add_product(product)


def test_get_products():
    products = ProductDBManager.get_all_products()
    products_string = ""
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


@app.route('/x')
def test_users():
    UserDBManager.create_table_user()

    return json.dumps(UserDBManager.get_user(1))


if __name__ == "__main__":
    app.run(debug=True)



