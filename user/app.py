import os
from flask import Flask
from flask_migrate import Migrate

from routes import user_blueprint
import models

app = Flask(__name__)

# Of course we'd never store the secret key in the code :eyes
app.config['SECRET_KEY'] = 'nBwg9uSus8m6kqApYqHUOQ'

file_path = os.path.abspath(os.getcwd())+"/database/user.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

models.init_app(app)

app.register_blueprint(user_blueprint)

migrate = Migrate(app, models.db)

if __name__ == "__main__":
    app.run()