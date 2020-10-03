# app/__init__.py
from flask import request, jsonify, abort, url_for, make_response
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

    def make_public_quote(quote):
        new_quote = {}
        for field in quote:
            if field == 'id':
                new_quote['uri'] = url_for('quotes', quote_id=quote['id'], _external=True)
                
            else:
                new_quote[field] = quote[field]
        return new_quote



    @app.route('/')
    def index():
        return 'Welcome to the quotes API!'


    @app.route('/vector/api/v1.0/quotes', methods=['POST', 'GET'])
    def quotes():

       
        if request.method == "POST":
            name = str(request.data.get('title', ''))
           
            quote = Quotes(name=name)
            quote.save()
            response = jsonify({
                    'id': quote.id,
                    'title': quote.name,
                    'date_created': quote.date_created,
                    'description': quote.description,
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
                    'description': quote.description,
                    'author': quote.author,
                }
                results.append(obj)
            response = jsonify([make_public_quote(quote) for quote in results])
            response.status_code = 200
            return response

    @app.route('/vector/api/v1.0/quotes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def quotes_manipulation(id, **kwargs):
     # retrieve a buckelist using it's ID
        quote = Quotes.query.filter_by(id=id).first()
        if not quote:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            quote.delete()
            return {
            "message": "quote {} deleted successfully".format(quote.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('title', ''))
            quote.name = name
            quote.save()
            response = jsonify({
                    'id': quote.id,
                    'title': quote.name,
                    'date_created': quote.date_created,
                    'description': quote.description,
                    'author': quote.author,
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                    'id': quote.id,
                    'title': quote.title,
                    'date_created': quote.date_created,
                    'description': quote.description,
                    'author': quote.author,
            })

            
            response.status_code = 200
            return response

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'OOPS! Quote not found'}), 404)

       


    return app