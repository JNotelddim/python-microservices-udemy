import base64
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
login_manager = LoginManager(app)

migrate = Migrate(app, models.db)

@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user


    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

if __name__ == "__main__":
    app.run()