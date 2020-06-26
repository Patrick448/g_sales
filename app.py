import json
import logging
from flask import Flask, request, render_template
from data.data import DataManager
from utils.db_manager import OrderDBManager

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('app')

app = Flask(__name__)

OrderDBManager.create_table_orders()

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

    return json.dumps(DataManager.get_today_list())


#@app.route('/save-order', methods=['POST'])
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


if __name__ == "__main__":
    app.run(debug=True)