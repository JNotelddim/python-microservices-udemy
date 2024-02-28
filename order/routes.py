from flask import Blueprint, request, jsonify, make_response
import requests

from models import Order

order_blueprint = Blueprint('order_api_route', __name__, url_prefix="/api/order")

USER_API_URL = 'http://127.0.0.1:5001/user/api'

def get_user(api_key):
    headers = {
        'Authorization': api_key,
    }

    response = requests.get(USER_API_URL, headers=headers)
    if response.status_code != 200:
        return { 'message': 'Not Authorized'}

    user = response.json()
    return user

@order_blueprint.route('/', methods=['GET'])
def get_open_order():
    return "Open order"

@order_blueprint.route('/all', methods=['GET'])
def get_all_orders():
    all_orders = Order.query.all()
    result = [order.serialize() for order in all_orders]
    return jsonify(result)

@order_blueprint.route('/add-item', methods=['POST'])
def add_order_item():
    return "adding item"

@order_blueprint.route('/checkout', methods=['POST'])
def checkout():
    return "checkout"
