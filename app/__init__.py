# app/__init__.py
from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Quotes

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Welcome to the quotes API!'


    @app.route('/vector/api/v1.0/quotes', methods=['POST', 'GET'])
    def quotes():
        if request.method == "POST":
            title = str(request.data.get('title', ''))
            description = str(request.data.get('description', ''))
            author = str(request.data.get('author', ''))
            if title:
                quote = Quotes(title=title, description=description, author=author)
                quote.save()
                response = jsonify({
                    'id': quotes[-1]['id'] + 1,
                    'title': quote.title,
                    'date_created': quote.date_created,
                    'description': quote.descricption,
                    'author': quote.author,

                })
                response.status_code = 201
                return response
        else:
            # GET
            quotes = Quotes.get_all()
            results = []

            for quote in quotes:
                obj = {
                    'id': quote.id,
                    'title': quote.title,
                    'date_created': quote.date_created,
                    'description': quote.descricption,
                    'author': quote.author,
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response


    return app