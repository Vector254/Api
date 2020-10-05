from flask import request, jsonify, abort, url_for, make_response, render_template
from flask_api import FlaskAPI
from .. import db
from . import main
from ..models import Quotes


def make_public_quote(quote):
        new_quote = {}
        for field in quote:
            if field == 'id':
                new_quote['uri'] = url_for('main.quotes', quote_id=quote['id'], _external=True)
                
            else:
                new_quote[field] = quote[field]
        return new_quote



@main.route('/')
def index():
    return render_template('index.html')


@main.route('/vector/api/v1.0/quotes', methods=['POST', 'GET'])
def quotes():

       
    if request.method == "POST":
        title = str(request.data.get('title', ''))
        author = str(request.data.get('author', ''))
        description = str(request.data.get('description', ''))
           
        quote = Quotes(name=title)
        quote.save()
        response = jsonify({
                'id': quote.id,
                'title': quote.title,
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

@main.route('/vector/api/v1.0/quotes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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
        title = str(request.data.decode.get('title', ''))
        author = str(request.data.get('author', ''))
        description = str(request.data.get('description', ''))
        date_created = str(request.data.get('date_created', ''))
        quote.title = title
        quote.author = author
        quote.description = description
        quote.date_created = date_created

        quote.save()
        response = jsonify({
                'id': quote.id,
                'title': quote.title,
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

