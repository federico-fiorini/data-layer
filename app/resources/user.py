from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.user import User
from app.common.utils import assign

user_fields = {
    'name': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'addresses': fields.Url('user_addresses', absolute=True),
    'orders': fields.Url('user_orders', absolute=True)
}

user_list_fields = {
    'name': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'addresses': fields.Url('user_addresses', absolute=True),
    'orders': fields.Url('user_orders', absolute=True),
    'url': fields.Url('user', absolute=True)
}


class UserListAPI(Resource):
    """
    Resource to manage users
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='No name provided', location='json')
        self.parser.add_argument('lastname', type=str, required=True, help='No last name provided', location='json')
        self.parser.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.parser.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(UserListAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_list_fields, envelope='users')
    def get(self):
        # Return all users
        return User.get_all()

    @auth.login_required
    @marshal_with(user_list_fields, envelope='user')
    def post(self):
        # Create new user
        args = self.parser.parse_args()
        user = User(name=args['name'], lastname=args['lastname'], email=args['email'], password=args['password'])

        # Persist and return user
        success = user.persist()
        if not success:
            abort(400, "User already exists")

        return user, 201


class UserAPI(Resource):
    """
    Resource to manage individual user
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('lastname', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        self.parser.add_argument('password', type=str, location='json')
        super(UserAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def get(self, user_id):
        # Get user by id
        user = User.get_by_id(user_id)
        if user is None:
            abort(404)

        # Return user
        return user

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def put(self, user_id):
        # Get user by id
        user = User.get_by_id(user_id)
        if user is None:
            abort(404)

        # Update user fields
        args = self.parser.parse_args()
        user.name = assign(args['name'], user.name)
        user.lastname = assign(args['lastname'], user.lastname)
        user.email = assign(args['email'], user.email)
        user.password = assign(args['password'], user.password)

        # Persist changes and return user
        user.persist()
        return user

    @auth.login_required
    def delete(self, user_id):
        # Delete user
        success = User.delete_by_id(user_id)
        if not success:
            abort(404)

        return {'result': True}

class UserAuthenticateAPI(Resource):
    """
    Resource to manage user authentication
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.parser.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(UserAuthenticateAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_list_fields, envelope='user')
    def post(self):
        args = self.parser.parse_args()

        # Get user by email
        user = User.get_by_email(args['email'])
        if user is None:
            abort(404)

        # Check password
        if args['password'] != user.password:
            abort(400)

        return user