from app import app
from flask import make_response, jsonify
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    if token == app.config['AUTHORIZATION_KEY']:
        return True
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)