import json

from flask import Flask, request, render_template
from data.data import DataManager
from utils.db_manager import OrderDBManager

app = Flask(__name__)

OrderDBManager.create_table_orders()

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
    return DataManager.get_all_orders()


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