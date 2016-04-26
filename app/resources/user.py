from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with

users = [
    {
        'id': 1,
        'name': u'Charles',
        'lastName': u'Ferrari',
        'email': u'charlesferrari@gmail.com'
    },
    {
        'id': 2,
        'name': u'Federico',
        'lastName': u'Fiorini',
        'email': u'fedefiorini@gmail.com'
    }
]

user_fields = {
    'name': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'uri': fields.Url('user')
}

class UserListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='No name provided', location='json')
        self.parser.add_argument('lastName', type=str, required=True, help='No last name provided', location='json')
        self.parser.add_argument('email', type=str, default="", location='json')
        super(UserListAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_fields, envelope='users')
    def get(self):
        # GET USERS : TODO from database
        return users

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def post(self):
        # CREATE USERS : TODO from database
        user = {'id': users[-1]['id'] + 1}
        args = self.parser.parse_args()
        for k, v in args.iteritems():
            if v is not None:
                user[k] = v

        users.append(user)
        return user, 201

class UserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('lastName', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        super(UserAPI, self).__init__()

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def get(self, id):
        # GET USER : TODO from database
        user = filter(lambda t: t['id'] == id, users)
        if len(user) == 0:
            abort(404)

        return user

    @auth.login_required
    @marshal_with(user_fields, envelope='user')
    def put(self, id):
        # GET USER : TODO from database
        user = filter(lambda t: t['id'] == id, users)
        if len(user) == 0:
            abort(404)
        user = user[0]
        args = self.parser.parse_args()
        for k, v in args.iteritems():
            if v is not None:
                user[k] = v

        return user

    @auth.login_required
    def delete(self, id):
        # GET USER : TODO from database
        user = filter(lambda t: t['id'] == id, users)
        if len(user) == 0:
            abort(404)
        users.remove(user[0])
        return {'result': True}
