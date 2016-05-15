from app.resources import auth
from flask_restful import Resource, fields, marshal_with

index_fields = {
    'users': fields.Url('users', absolute=True),
    'addresses': fields.Url('addresses', absolute=True),
    'cleaners': fields.Url('cleaners', absolute=True),
    'services': fields.Url('services', absolute=True),
    'orders': fields.Url('orders', absolute=True),
    'schedules': fields.Url('schedules', absolute=True)
}


class IndexAPI(Resource):
    """
    Resource to expose apis
    """

    @auth.login_required
    @marshal_with(index_fields, envelope='apis')
    def get(self):
        return self