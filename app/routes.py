from app import api
from app.resources.user import UserListAPI, UserAPI

# Users endpoints
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint='users')
api.add_resource(UserAPI, '/api/v1.0/users/<int:id>', endpoint='user')
