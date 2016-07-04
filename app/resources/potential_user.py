from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.potential_user import PotentialUser
from app.common.utils import assign

potential_user_fields = {
    'email': fields.String,
    'zip': fields.String,
    'date': fields.String
}

potential_user_list_fields = {
    'email': fields.String,
    'zip': fields.String,
    'date': fields.String,
    'url': fields.Url('potential_user', absolute=False)
}


class PotentialUserListAPI(Resource):

    """
    Resource to manage potential users
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.parser.add_argument('zip', type=str, required=True, help='No zip code provided', location='json')
        self.parser.add_argument('date', type=str, required=True, help='No date provided', location='json')
        super(PotentialUserListAPI, self).__init__()

    @auth.login_required
    @marshal_with(potential_user_list_fields, envelope='potential_users')
    def get(self):
        # Return all potential users
        return PotentialUser.get_all()

    @auth.login_required
    @marshal_with(potential_user_list_fields, envelope='potential_user')
    def post(self):
        # Create new potential user
        args = self.parser.parse_args()
        potential_user = PotentialUser(email=args['email'], zip=args['zip'], date=args['date'])

        # Persist and return potential user
        success = potential_user.persist()
        if not success:
            abort(400, "PotentialUser already stored")

        return potential_user, 201


class PotentialUserAPI(Resource):
    """
    Resource to manage individual potential_user
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, location='json')
        self.parser.add_argument('zip', type=str, location='json')
        self.parser.add_argument('date', type=str, location='json')
        super(PotentialUserAPI, self).__init__()

    @auth.login_required
    @marshal_with(potential_user_fields, envelope='potential_user')
    def get(self, potential_user_id):
        # Get potential user by id
        potential_user = PotentialUser.get_by_id(potential_user_id)
        if potential_user is None:
            abort(404)

        # Return potential user
        return potential_user

    @auth.login_required
    @marshal_with(potential_user_fields, envelope='potential_user')
    def put(self, potential_user_id):
        # Get potential user by id
        potential_user = PotentialUser.get_by_id(potential_user_id)
        if potential_user is None:
            abort(404)

        # Update potential user fields
        args = self.parser.parse_args()
        potential_user.email = assign(args['email'], potential_user.email)
        potential_user.date = assign(args['date'], potential_user.date)
        potential_user.email = assign(args['email'], potential_user.email)

        # Persist changes and return potential user
        potential_user.persist()
        return potential_user

    @auth.login_required
    def delete(self, potential_user_id):
        # Delete potential user
        success = PotentialUser.delete_by_id(potential_user_id)
        if not success:
            abort(404)

        return {'result': True}