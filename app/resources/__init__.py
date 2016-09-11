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

# Import all resources
from app.resources.index import *
from app.resources.address import *
from app.resources.cleaner import *
from app.resources.order import *
from app.resources.schedule import *
from app.resources.service import *
from app.resources.user import *
from app.resources.potential_user import *
from app.resources.coverage import *