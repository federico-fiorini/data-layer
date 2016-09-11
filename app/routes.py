from app import api
from app.resources import *


# Index
api.add_resource(IndexAPI, '/', endpoint='index')

# Services type endpoint
api.add_resource(ServiceListAPI, '/api/v1.0/services', endpoint='services')

# Users endpoints
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint='users')
api.add_resource(UserAuthenticateAPI, '/api/v1.0/user/authentication', endpoint='user_authentication')
api.add_resource(UserAPI, '/api/v1.0/user/<int:user_id>', endpoint='user')
api.add_resource(AddressListByUserAPI, '/api/v1.0/user/<int:user_id>/addresses', endpoint='user_addresses')
api.add_resource(OrderListByUserAPI, '/api/v1.0/user/<int:user_id>/orders', endpoint='user_orders')

# Addresses endpoints
api.add_resource(AddressListAPI, '/api/v1.0/addresses', endpoint='addresses')
api.add_resource(AddressAPI, '/api/v1.0/address/<int:address_id>', endpoint='address')
api.add_resource(OrderListByAddressAPI, '/api/v1.0/address/<int:address_id>/orders', endpoint='address_orders')

# Cleaners endpoints
api.add_resource(CleanerListAPI, '/api/v1.0/cleaners', endpoint='cleaners')
api.add_resource(CleanerAPI, '/api/v1.0/cleaner/<int:cleaner_id>', endpoint='cleaner')
api.add_resource(ScheduleListByCleanerAPI, '/api/v1.0/cleaner/<int:cleaner_id>/schedule', endpoint='cleaner_schedule')
api.add_resource(OrderListByCleanerAPI, '/api/v1.0/cleaner/<int:cleaner_id>/orders', endpoint='cleaner_orders')
api.add_resource(CoverageListByCleanerAPI, '/api/v1.0/cleaner/<int:cleaner_id>/coverages', endpoint='cleaner_coverages')
api.add_resource(CoverageAPI, '/api/v1.0/cleaner/<int:cleaner_id>/coverage/<int:zip>', endpoint='cleaner_coverage')

# Schedule endpoints
api.add_resource(ScheduleListAPI, '/api/v1.0/schedules', endpoint='schedules')
api.add_resource(ScheduleAPI, '/api/v1.0/schedule/<int:schedule_id>', endpoint='schedule')

# Order endpoints
api.add_resource(OrderListAPI, '/api/v1.0/orders', endpoint='orders')
api.add_resource(OrderAPI, '/api/v1.0/order/<int:order_id>', endpoint='order')
api.add_resource(OrderByReferenceAPI, '/api/v1.0/order/reference/<string:reference>', endpoint='order_reference')

# Prospettive users endpoints
api.add_resource(PotentialUserAPI, '/api/v1.0/potential_user/<int:potential_user_id>', endpoint='potential_user')
api.add_resource(PotentialUserListAPI, '/api/v1.0/potential_users', endpoint='potential_users')

# Coverage endpoints
api.add_resource(CoverageListAPI, '/api/v1.0/coverages', endpoint='coverages')
