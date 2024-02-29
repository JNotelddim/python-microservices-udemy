from flask import Blueprint, render_template, session, redirect
from flask_login import current_user

from api.book_client import BookClient
from api.order_client import OrderClient
from api.user_api import UserClient

blueprint = Blueprint('frontend', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()

    try:
        books = BookClient.get_books()
    except:
        books = {'result': []}

    return render_template('index.html', books=books)