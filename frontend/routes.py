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

    print('method ' + request.method)
    if request.method == 'POST':
        print(f'validate {str(form.validate_on_submit())}')
        if form.validate_on_submit():
            username = form.username.data

            print('User exists: '+ str(UserClient.user_exists(username)))
            if UserClient.user_exists(username):
                flash("Uesrname taken.")
                return render_template('register.html', form=form)
            else:
                user = UserClient.create_user(form)
                print('Created user: ' + str(user))
                if user:
                    flash("Registered. Please login.")
                    return redirect(url_for('frontend.login'))
                else:
                    return render_template('register.html', form=form)
        else:
            print('Other errors.')
            flash('Errors')
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)