from flask import Flask
import os
from flask_migrate import Migrate

from routes import book_blueprint
from models import db, Book, init_app

app = Flask(__name__)
app.config['SECRET_KEY'] = "WtlLAh2AZllfQkitoY6KqA"

file_path = os.path.abspath(os.getcwd())+"/database/book.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

init_app(app)

app.register_blueprint(book_blueprint)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)