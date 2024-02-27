import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'nBwg9uSus8m6kqApYqHUOQ'

file_path = os.path.abspath(os.getcwd())+"/database/order.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

# models.init_app(app)

# app.register_blueprint(user_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=5003)