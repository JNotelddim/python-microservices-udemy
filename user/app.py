from flask import Flask

from routes import user_blueprint
import models

app = Flask(__name__)

# Of course we'd never store the secret key in the code :eyes
app.config['SECRET_KEY'] = 'nBwg9uSus8m6kqApYqHUOQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'
models.init_app(app)
app.register_blueprint(user_blueprint)

app.run()