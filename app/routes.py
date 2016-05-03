from app import api
from app.resources.user import *
from app.resources.address import *

# Users endpoints
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint='users')
api.add_resource(UserAPI, '/api/v1.0/user/<int:id>', endpoint='user')
api.add_resource(AddressListByUserAPI, '/api/v1.0/user/<int:id>/addresses', endpoint='user_addresses')
api.add_resource(AddressListAPI, '/api/v1.0/addresses', endpoint='addresses')
api.add_resource(AddressAPI, '/api/v1.0/address/<int:id>', endpoint='address')

