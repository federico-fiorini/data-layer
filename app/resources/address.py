from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.address import Address
from app.models.user import User
from app.common.utils import assign

address_fields = {
    'street': fields.String,
    'house_number': fields.String,
    'flat_number': fields.String,
    'post_code': fields.String,
    'city': fields.String,
    'country': fields.String,
    'neighbourhood': fields.String,
    'orders': fields.Url('address_orders', absolute=False)
}

address_list_fields = address_fields.copy()
address_list_fields['url'] = fields.Url('address', absolute=False)


class AddressAPI(Resource):
    """
    Resource to manage user individual address
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('street', type=str, required=False, location='json')
        self.parser.add_argument('house_number', type=str, required=False, location='json')
        self.parser.add_argument('flat_number', type=str, required=False, location='json')
        self.parser.add_argument('post_code', type=str,  required=False, location='json')
        self.parser.add_argument('city', type=str,  required=False, location='json')
        self.parser.add_argument('country', type=str,  required=False, location='json')
        self.parser.add_argument('neighbourhood', type=str, required=False, location='json')
        super(AddressAPI, self).__init__()

    @auth.login_required
    @marshal_with(address_fields, envelope='address')
    def get(self, address_id):
        # Get address by id
        address = Address.get_by_id(address_id)
        if address is None:
            abort(404)

        # Return address
        return address

    @auth.login_required
    @marshal_with(address_fields, envelope='address')
    def put(self, address_id):
        # Get address by id
        address = Address.get_by_id(address_id)
        if address is None:
            abort(404)

        # Update address fields
        args = self.parser.parse_args()
        address.street = assign(args['street'], address.street)
        address.house_number = assign(args['house_number'], address.house_number)
        address.flat_number = assign(args['flat_number'], address.flat_number)
        address.post_code = assign(args['post_code'], address.post_code)
        address.city = assign(args['city'], address.city)
        address.country = assign(args['country'], address.country)
        address.neighbourhood = assign(args['neighbourhood'], address.neighbourhood)

        # Persist changes and return address
        address.persist()
        return address

    @auth.login_required
    def delete(self, address_id):
        # Delete address
        success = Address.delete_by_id(address_id)
        if not success:
            abort(404)

        return {'result': True}


class AddressListAPI(Resource):
    """
    Resource to manage user addresses list
    """

    @auth.login_required
    @marshal_with(address_list_fields, envelope='addresses')
    def get(self):
        # Return all user's addresses
        return Address.get_all()


class AddressListByUserAPI(Resource):
    """
    Resource to manage user addresses list
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('street', type=str, required=True, help='No street provided', location='json')
        self.parser.add_argument('house_number', type=str, required=True, help='No house number provided', location='json')
        self.parser.add_argument('flat_number', type=str, required=False, location='json')
        self.parser.add_argument('post_code', type=str,  required=True, help='No post code provided', location='json')
        self.parser.add_argument('city', type=str,  required=True, help='No city provided', location='json')
        self.parser.add_argument('country', type=str,  required=True, help='No country provided', location='json')
        self.parser.add_argument('neighbourhood', type=str, required=False, default='', location='json')
        super(AddressListByUserAPI, self).__init__()

    @auth.login_required
    @marshal_with(address_list_fields, envelope='addresses')
    def get(self, user_id):
        # Return all user's addresses
        return Address.get_all_by_user(user_id)

    @auth.login_required
    @marshal_with(address_list_fields, envelope='address')
    def post(self, user_id):

        # Validate user
        if User.get_by_id(user_id) is None:
            abort(404, 'User not found')

        # Create new address
        args = self.parser.parse_args()
        address = Address(user_id=user_id, street=args['street'], house_number=args['house_number'], city=args['city'],
                          post_code=args['post_code'], flat_number=args['flat_number'], country=args['country'],
                          neighbourhood=args['neighbourhood'])

        # Persist and return address
        address.persist()
        return address, 201
