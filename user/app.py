import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from routes import user_blueprint
import models

app = Flask(__name__)

# Of course we'd never store the secret key in the code :eyes
app.config['SECRET_KEY'] = 'nBwg9uSus8m6kqApYqHUOQ'

file_path = os.path.abspath(os.getcwd())+"/database/user.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

models.init_app(app)

app.register_blueprint(user_blueprint)
login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, models.db)

@login_manager.user_loader
def load_user(user_id):
    print(f'[user loader] Loading user with id: {user_id}...')
    user = models.User.query.filter_by(id=user_id).first()
    print(f'[user loader] Found user: {user}')
    return user


@login_manager.request_loader
def load_user(request):
    print(f'[request loader] Loading user by token value...')
    token = request.headers.get('Authorization')
    user_by_token = models.User.query.filter_by(api_key=token).first()
    if not user_by_token:
        print(f'[request loader] No user found for token value: {user_by_token}')
        return None
    else:
        print(f'[request loader] Found user {user_by_token}')
        return user_by_token

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)