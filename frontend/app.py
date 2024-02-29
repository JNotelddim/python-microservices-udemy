from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from routes import blueprint

app = Flask(__name__, static_folder='static')

app.config['SECRET'] = 'nBwg9uSus8m6kqApYqHUOQ'
app.config['WTF_CSRF_SECRET_KEY'] = 'nBwg9uSus8m6kqApYqHUOQ'
app.config['UPLOAD_FOLDER'] = 'static/images'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_message = "Please login."
login_manager.login_view = 'frontend.login'
app.register_blueprint(blueprint)

bootstrap = Bootstrap(app)

@login_manager.user_loader
def load_user(user_id):
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)