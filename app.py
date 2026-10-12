"""Small Flask API for the ACEest DevOps lab; records are held in memory."""
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from services import PROGRAMS, calorie_target


def create_app():
    app = Flask(__name__)
    clients = {}

    @app.get('/')
    def index():
        return jsonify(application='ACEest Fitness and Gym',
                       endpoints=['/health', '/programs', '/clients'])

    @app.get('/health')
    def health():
        return jsonify(status='ok')

    @app.get('/programs')
    def programs():
        return jsonify(PROGRAMS)

    @app.get('/clients')
    def list_clients():
        return jsonify(list(clients.values()))

    @app.post('/clients')
    def add_client():
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error='A JSON object is required'), 400
        name = data.get('name')
        if not isinstance(name, str) or not name.strip():
            return jsonify(error='Name is required'), 400
        name = name.strip()
        if len(name) > 100:
            return jsonify(error='Name must be at most 100 characters'), 400
        program = data.get('program')
        if not isinstance(program, str):
            return jsonify(error='Program must be FL, MG or BG'), 400
        try:
            calories = calorie_target(data.get('weight'), program)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        if name in clients:
            return jsonify(error='Client already exists'), 409
        record = {'name': name, 'weight': data['weight'], 'program': program,
                  'calories': calories, 'progress': []}
        clients[name] = record
        return jsonify(record), 201

    @app.get('/clients/<name>')
    def get_client(name):
        if name not in clients:
            return jsonify(error='Client not found'), 404
        return jsonify(clients[name])

    @app.post('/clients/<name>/progress')
    def add_progress(name):
        if name not in clients:
            return jsonify(error='Client not found'), 404
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error='A JSON object is required'), 400
        adherence = data.get('adherence')
        if type(adherence) is not int or not 0 <= adherence <= 100:
            return jsonify(error='Adherence must be an integer from 0 to 100'), 400
        clients[name]['progress'].append({'adherence': adherence})
        return jsonify(clients[name]), 201

    @app.errorhandler(HTTPException)
    def http_error(exc):
        return jsonify(error=exc.description), exc.code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
