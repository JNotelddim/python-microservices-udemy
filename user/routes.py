from flask import Blueprint, jsonify, request, make_response
from models import db, User
from flask_login import login_user
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

@user_blueprint.route('login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]

    existing_user = User.query.filter_by(username=username).first()

    if not existing_user:
        return make_response(jsonify({'message': 'Username not found.'}), 401)

    if check_password_hash(existing_user.password, password):
        existing_user.update_api_key()
        db.session.commit()
        login_user(existing_user)
        response = {'message': 'Logged in.', 'api_key': existing_user.api_key}
        return make_response(jsonify(response), 200)

    return make_response(jsonify({'message': 'Access denied.'}), 401)