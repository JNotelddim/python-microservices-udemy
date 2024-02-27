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
    print(f'loading user with id: {user_id}...')
    user = models.User.query.filter_by(id=user_id).first()
    print(f'found user: {user}')
    return user

if __name__ == "__main__":
    app.run(debug=True, port=5001)