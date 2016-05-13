from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.service import Service
from app.common.utils import assign

service_fields = {
    'type': fields.String,
    'name': fields.String,
    'time': fields.String
}


class ServiceListAPI(Resource):
    """
    Resource to manage services type
    """

    @auth.login_required
    @marshal_with(service_fields, envelope='services')
    def get(self):
        # Return all users
        return Service.get_all()
