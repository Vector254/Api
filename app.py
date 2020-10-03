#!rest/bin/python
from flask import Flask, jsonify, abort, make_response
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
    return jsonify({'quotes': quotes})



@app.route('/vector/api/v1.0/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    quote = [quote for quote in quotes if quote['id'] == quote_id]
    if len(quote) == 0:
        abort(404)
    return jsonify({'quote': quote[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'OOPS! Quote not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

