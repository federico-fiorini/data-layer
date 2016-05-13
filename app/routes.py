from app import api
from app.resources import *


# Index
api.add_resource(IndexAPI, '/', endpoint='index')

# Services type endpoint
api.add_resource(ServiceListAPI, '/api/v1.0/services', endpoint='services')

# Users endpoints
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint='users')
api.add_resource(UserAPI, '/api/v1.0/user/<int:id>', endpoint='user')
api.add_resource(AddressListByUserAPI, '/api/v1.0/user/<int:id>/addresses', endpoint='user_addresses')
api.add_resource(OrderListByUserAPI, '/api/v1.0/user/<int:id>/orders', endpoint='user_orders')

# Addresses endpoints
api.add_resource(AddressListAPI, '/api/v1.0/addresses', endpoint='addresses')
api.add_resource(AddressAPI, '/api/v1.0/address/<int:id>', endpoint='address')
api.add_resource(OrderListByAddressAPI, '/api/v1.0/address/<int:id>/orders', endpoint='address_orders')

# Cleaners endpoints
api.add_resource(CleanerListAPI, '/api/v1.0/cleaners', endpoint='cleaners')
api.add_resource(CleanerAPI, '/api/v1.0/cleaner/<int:id>', endpoint='cleaner')
api.add_resource(SheduleListByCleanerAPI, '/api/v1.0/cleaner/<int:id>/shedule', endpoint='cleaner_schedule')
api.add_resource(OrderListByCleanerAPI, '/api/v1.0/cleaner/<int:id>/orders', endpoint='cleaner_orders')

# Schedule endpoints
api.add_resource(ScheduleListAPI, '/api/v1.0/schedules', endpoint='schedules')
api.add_resource(ScheduleAPI, '/api/v1.0/schedule/<int:id>', endpoint='schedule')

# Order endpoints
api.add_resource(OrderListAPI, '/api/v1.0/orders', endpoint='orders')
api.add_resource(OrderAPI, '/api/v1.0/order/<int:id>', endpoint='order')