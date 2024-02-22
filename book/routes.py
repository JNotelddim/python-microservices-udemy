from flask import Blueprint, request, jsonify

from models import Book, db

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    all_books = Book.query.all()

    result = [book.serialize() for book in all_books]

    response = {"result": result}
    return jsonify(response)

@book_blueprint.route('/create', methods=['POST'])
def create_books():
    try:
        new_book = Book()
        new_book.name = request.form['name']
        new_book.slug = request.form['slug']
        new_book.image = request.form['image']
        new_book.price = request.form['price']

        db.session.add(new_book)
        db.session.commit()

        response = {'message': 'Book created.', 'result': new_book.serialize()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Book creation failed.'}

    return jsonify(response)

@book_blueprint.route('/<slug>', methods=['GET'])
def book_details(slug):
    print(slug)
    book = Book.query.filter_by(slug=slug).first()

    if book:
        response  = { 'result': book.serialize() }
    else:
        response = { 'message': 'No books found'}

    return jsonify(response)