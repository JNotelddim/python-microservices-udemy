from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from flask_login import current_user

import forms
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

@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = forms.RegistrationForm(request.form)

    print('[Frontend Register] method ' + request.method)
    if request.method == 'POST':
        print(f'validate {str(form.validate_on_submit())}')
        if form.validate_on_submit():
            username = form.username.data

            print('[Frontend Register] User exists: '+ str(UserClient.user_exists(username)))
            if UserClient.user_exists(username):
                flash("Uesrname taken.")
                return render_template('register.html', form=form)
            else:
                user = UserClient.create_user(form)
                print('[Frontend Register]Created user: ' + str(user))
                if user:
                    flash("Registered. Please login.")
                    return redirect(url_for('frontend.login'))
                else:
                    return render_template('register.html', form=form)
        else:
            print('[Frontend Register] Other errors.')
            flash('Errors')
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_key = UserClient.login(form)
            print(f'[Frontend login] api_key: {api_key}')

            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                print(f'[Frontend login] user: {user}, api_key: {api_key}')
                session['user'] = user

                flash('Welcome back.')
                return redirect(url_for('frontend.index'))
            else:
                flash("Cannot log in.")

        else:
            flash("Cannot log in.")

    return render_template('login.html', form=form)

@blueprint.route('/logout', methods=['GET'])
def logout():
    UserClient.logout()
    session.clear()
    flash('Logged out.')
    # what about UserClient.logout?
    return redirect(url_for('frontend.index'))

@blueprint.route('/book/<slug>', methods=['GET', 'POST'])
def book_details(slug):
    response = BookClient.get_book(slug).json()
    book = response['result']

    form = forms.ItemForm(book_id=book['id'])

    if request.method == 'POST':
        print('[Frontend Bookdetails]' + str(session))
        if 'user' not in session:
            flash('Please log in')
            return redirect(url_for('frontend.login'))

        order = OrderClient.add_to_cart(book_id=book['id'], quantity=1)

        # if order['message'] == 'Not logged in':
            # return redirect(url_for('frontend.login'))

        print(f'[Frontend bookdetails] order: {order}')
        session['session'] = order['result']
        flash('Book added to the cart')

    return render_template('book_info.html', book=book, form=form)