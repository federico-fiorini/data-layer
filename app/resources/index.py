from app.resources import auth
from flask_restful import Resource, fields, marshal_with

index_fields = {
    'users': fields.Url('users', absolute=False),
    'user_authentication': fields.Url('user_authentication', absolute=False),
    'potential_users': fields.Url('potential_users', absolute=False),
    'addresses': fields.Url('addresses', absolute=False),
    'cleaners': fields.Url('cleaners', absolute=False),
    'services': fields.Url('services', absolute=False),
    'orders': fields.Url('orders', absolute=False),
    'order_reference': fields.Url('order_reference', absolute=False),
    'schedules': fields.Url('schedules', absolute=False)

}


class IndexAPI(Resource):
    """
    Resource to expose apis
    """

    @auth.login_required
    @marshal_with(index_fields, envelope='apis')
    def get(self):
        return IndexFields()


class IndexFields:
    def __init__(self):
        self.reference = "REFERENCE_NUMBER"
