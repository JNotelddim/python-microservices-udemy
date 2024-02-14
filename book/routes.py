from flask import Blueprint, request, jsonify

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    return "all bokoks"

@book_blueprint.route('/create', methods=['POST'])
def create_books():
        return "book created"

@book_blueprint.route('/<slug>', methods=['GET'])
def book_details(slug):
    return "book details " + slug