from flask import Flask
import os

from routes import book_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = "WtlLAh2AZllfQkitoY6KqA"
file_path = os.path.abspath(os.getcwd())+"/database/book.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

app.register_blueprint(book_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=5002)