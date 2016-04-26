from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.user import User
from app.common.utils import assign

user_fields = {
    'name': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'uri': fields.Url('user')
}

class UserListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='No name provided', location='json')
        self.parser.add_argument('lastname', type=str, required=True, help='No last name provided', location='json')
        self.parser.add_argument('email', type=str, default="", location='json')
        super(UserListAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_fields, envelope='users')
    def get(self):
        # Return all users
        return User.get_all()

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def post(self):
        # Create new user
        args = self.parser.parse_args()
        user = User(args['name'], args['lastname'], args['email'])

        # Persist and return user
        user.persist()
        return user, 201

class UserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('lastname', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        super(UserAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def get(self, id):
        # Get user by id
        user = User.get_by_id(id)
        if user is None:
            abort(404)

        # Return user
        return user

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def put(self, id):
        # Get user by id
        user = User.get_by_id(id)
        if user is None:
            abort(404)

        # Update user fields
        args = self.parser.parse_args()
        user.name = assign(args['name'], user.name)
        user.lastname = assign(args['lastname'], user.lastname)
        user.email = assign(args['email'], user.email)

        # Persist changes and return user
        user.persist()
        return user

    @auth.login_required
    def delete(self, id):
        # Delete user
        success = User.delete_by_id(id)
        if not success:
            abort(404)

        return {'result': True}
