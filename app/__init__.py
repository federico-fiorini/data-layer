from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

from app import routes

from app.database import db_session, init_db

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
