from flask import Blueprint, jsonify, request, make_response
from models import db, User
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/user')


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = [user.serialize() for user in all_users]
    response = {
        'message': 'Returning all users.',
        'result': result
    }

    return jsonify(response)

@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        new_user = User()
        new_user.username = request.form["username"]
        new_user.password = generate_password_hash(request.form["password"]) #, method="sha256")
        new_user.is_admin = True # only cause this is dev.

        db.session.add(new_user)
        db.session.commit()

        response = {'message': "User created.", 'result': new_user.serialize()}
    except Exception as e:
        print(e)
        response = { 'message': "Error creating user."}
    return jsonify(response)

@user_blueprint.route('/login', methods=['POST'])
def login():
    print(f'[User login] ...')
    username = request.form["username"]
    password = request.form["password"]

    existing_user = User.query.filter_by(username=username).first()

    if not existing_user:
        print('[User login] User does not exist.')
        return make_response(jsonify({'message': 'Username not found.'}), 401)

    if check_password_hash(existing_user.password, password):
        existing_user.update_api_key()
        # Set is_active?
        db.session.commit()
        print('[User login]logging in user:', existing_user)
        login_user(existing_user)
        response = {'message': 'Logged in.', 'api_key': existing_user.api_key}
        print(f'[User login] returning response: {response}')
        return make_response(jsonify(response), 200)

    print('[User login] logged in user:', current_user)

    return make_response(jsonify({'message': 'Access denied.'}), 401)



@user_blueprint.route('/logout', methods=['POST'])
def logout():
    print(f'[User logout] current_user: {current_user}')
    if current_user.is_authenticated:
        current_user.is_authenticated = False
        logout_user()
        db.session.commit()
        print('[User logout] logged out.')
        return jsonify({ 'message': 'Logged out.'})

    print(f'[User logout] logged in user: {current_user}')
    return make_response(jsonify({'message': 'No user logged in.'}), 401)

@user_blueprint.route('/<username>/exists', methods=['GET'])
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return make_response(jsonify({ 'result': True}), 200)

    return make_response(jsonify({'result': False}), 404)

@user_blueprint.route('/', methods=['GET'])
def get_current_user():
    print('[User]' + str(current_user))
    if current_user.is_authenticated:
        return make_response(jsonify({'result': current_user.serialize()}), 200)

    print(f'[User] user not authenticated')
    return make_response(jsonify({ 'message': 'Not logged in.'}), 401)