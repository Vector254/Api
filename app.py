#!rest/bin/python
from flask import Flask, jsonify
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

@app.route('/vector/api/v1.0/quotes', methods=['GET'])
def get_tasks():
    return jsonify({'quotes': quotes})

@app.route('/')
def index():
    return 'What a bright day!'


if __name__ == '__main__':
    app.run(debug=True)

