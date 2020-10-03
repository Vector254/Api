#!rest/bin/python
from flask import Flask, jsonify, abort, make_response,request, url_for
app = Flask(__name__)

quotes = [
    {
        'id': 1,
        'title': u'A new day',
        'description': u'Darkness may last for a night, but the sun will still rise', 
        'author': u'anonymous' 
    },
    {
        'id': 2,
        'title': u'never give up',
        'description': u'The day you give up, is the day you cease to live', 
        'author': u'vector'
    }
]

@app.route('/')
def index():
    return 'What a bright day!'

@app.route('/vector/api/v1.0/quotes', methods=['GET'])
def get_tasks():
    return jsonify({'quotes': [make_public_quote(quote) for quote in quotes]})



@app.route('/vector/api/v1.0/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    quote = [quote for quote in quotes if quote['id'] == quote_id]
    if len(quote) == 0:
        abort(404)
    return jsonify({'quote': [make_public_quote(quote[0])]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'OOPS! Quote not found'}), 404)

@app.route('/vector/api/v1.0/quotes', methods=['POST'])
def create_quote():
    if not request.json or not 'title' in request.json:
        abort(400)
    quote = {
        'id': quotes[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'author': request.json.get('author',"")
    }
    quotes.append(quote)
    return jsonify({'quote':[make_public_quote(quote)]}), 201

@app.route('/vector/api/v1.0/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    quote = [quote for quote in quotes if quote['id'] == quote_id]
    if len(quote) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'author' in request.json and type(request.json['author']) is not str:
        abort(400)
    quote[0]['title'] = request.json.get('title', quote[0]['title'])
    quote[0]['description'] = request.json.get('description', quote[0]['description'])
    quote[0]['title'] = request.json.get('author', quote[0]['author'])
    return jsonify({'quote': [make_public_quote(quote[0])]})

@app.route('/vector/api/v1.0/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    quote = [quote for quote in quotes if quote['id'] == quote_id]
    if len(quote) == 0:
        abort(404)
    quotes.remove(quote[0])
    return jsonify({'result': True})

def make_public_quote(quote):
    new_quote = {}
    for field in quote:
        if field == 'id':
            new_quote['uri'] = url_for('get_quote', quote_id=quote['id'], _external=True)
        else:
            new_quote[field] = quote[field]
    return new_quote

if __name__ == '__main__':
    app.run(debug=True)

