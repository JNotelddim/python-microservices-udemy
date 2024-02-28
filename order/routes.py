from flask import Blueprint, request, jsonify, make_response
import requests

order_blueprint = Blueprint('order_api_route', __name__, url_prefix="/api/order")

USER_API_URL = 'http://127.0.0.1:5001/user/api'

@order_blueprint.route('/', methods=['GET'])
def get_open_order():
    return "Open order"

@order_blueprint.route('/all', methods=['GET'])
def get_all_orders():
    return "all orders"

@order_blueprint.route('/add-item', methods=['POST'])
def add_order_item():
    return "adding item"

@order_blueprint.route('/checkout', methods=['POST'])
def checkout():
    return "checkout"
