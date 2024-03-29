from app.resources import auth
from flask import abort, request
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.order import Order
from app.models.address import Address
from app.models.cleaner import Cleaner
from app.models.user import User
from app.common.utils import assign, is_valid_date

order_fields = {
    'date': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'rooms': fields.String,
    'special_rooms': fields.String,
    'extra_services': fields.String,
    'reference': fields.String,
    'transaction': fields.String,
    'price': fields.String,
    'cleaner': fields.Url('cleaner', absolute=False),
    'user': fields.Url('user', absolute=False),
    'address': fields.Url('address', absolute=False)

}

order_list_fields = order_fields.copy()
order_list_fields['url'] = fields.Url('order', absolute=False)


class OrderAPI(Resource):
    """
    Resource to manage user individual address
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cleaner_id', type=str, required=False, location='json')
        self.parser.add_argument('address_id', type=str, required=False, location='json')
        self.parser.add_argument('date', type=str, required=False, location='json')
        self.parser.add_argument('start_time', type=str, required=False, location='json')
        self.parser.add_argument('end_time', type=str, required=False, location='json')
        self.parser.add_argument('rooms', type=str,  required=False, location='json')
        self.parser.add_argument('special_rooms', type=str,  required=False, location='json')
        self.parser.add_argument('extra_services', type=str,  required=False, location='json')
        self.parser.add_argument('reference', type=str, required=False, location='json')
        self.parser.add_argument('transaction', type=str, required=False, location='json')
        self.parser.add_argument('price', type=str, required=False, location='json')
        super(OrderAPI, self).__init__()

    @auth.login_required
    @marshal_with(order_fields, envelope='order')
    def get(self, order_id):
        # Get order by id
        order = Order.get_by_id(order_id)
        if order is None:
            abort(404)

        # Return order
        return order

    @auth.login_required
    @marshal_with(order_fields, envelope='order')
    def put(self, order_id):
        # Get order by id
        order = Order.get_by_id(order_id)
        if order is None:
            abort(404)

        # Update order fields
        args = self.parser.parse_args()
        order.cleaner_id = assign(args['cleaner_id'], order.cleaner_id)
        order.address_id = assign(args['address_id'], order.address_id)
        order.date = assign(args['date'], order.date)
        order.start_time = assign(args['start_time'], order.start_time)
        order.end_time = assign(args['end_time'], order.end_time)
        order.rooms = assign(args['rooms'], order.rooms)
        order.special_rooms = assign(args['special_rooms'], order.special_rooms)
        order.extra_services = assign(args['extra_services'], order.extra_services)
        order.reference = assign(args['reference'], order.reference)
        order.transaction = assign(args['transaction'], order.transaction)
        order.price = assign(args['price'], order.price)

        # Persist changes and return order
        order.persist()
        return order

    @auth.login_required
    def delete(self, order_id):
        # Delete order
        success = Order.delete_by_id(order_id)
        if not success:
            abort(404)

        return {'result': True}


class OrderByReferenceAPI(Resource):
    """
    Resource to return order by reference
    """
    @auth.login_required
    @marshal_with(order_list_fields, envelope='order')
    def get(self, reference):
        if reference is not None:
            # Try to get the orders from that reference otherwise returns an 404 error
            orders = Order.get_by_reference(reference)
            if orders:
                return orders
            abort(404)

        abort(400, 'Parameters incorrect')


class OrderListAPI(Resource):
    """
    Resource to manage orders list
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('from', type=str, required=False, location='args')
        self.parser.add_argument('to', type=str, required=False, location='args')
        self.parser.add_argument('payed', type=str, required=False, location='args')
        super(OrderListAPI, self).__init__()

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self):
        args = self.parser.parse_args()
        params = {k: v for k, v in args.items() if v is not None}

        if 'from' in params and not is_valid_date(params['from']):
            abort(400, 'Parameters incorrect')

        if 'to' in params and not is_valid_date(params['to']):
            abort(400, 'Parameters incorrect')

        return Order.get_all(params)


class OrderListByUserAPI(Resource):
    """
    Resource to manage user orders list
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cleaner_id', type=str, required=True, help='No cleaner provided', location='json')
        self.parser.add_argument('address_id', type=str, required=True, help='No address provided', location='json')
        self.parser.add_argument('date', type=str, required=True, help='No date provided', location='json')
        self.parser.add_argument('start_time', type=str, required=True, help='No start time provided', location='json')
        self.parser.add_argument('end_time', type=str, required=True, help='No end time provided', location='json')
        self.parser.add_argument('rooms', type=str, required=True, help='No number of rooms provided', location='json')
        self.parser.add_argument('special_rooms', type=str, required=False, default=None, location='json')
        self.parser.add_argument('extra_services', type=str, required=False, default=None, location='json')
        self.parser.add_argument('reference', type=str, required=False, default=None, location='json')
        self.parser.add_argument('transaction', type=str, required=False, default=None, location='json')
        self.parser.add_argument('price', type=str, required=True, default=None, location='json')
        super(OrderListByUserAPI, self).__init__()

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self, user_id):
        # Return all user's orders
        return Order.get_all_by_user(user_id)

    @auth.login_required
    @marshal_with(order_list_fields, envelope='order')
    def post(self, user_id):
        # Get arguments
        args = self.parser.parse_args()

        # Validate user, address and cleaner ids
        if User.get_by_id(user_id) is None:
            abort(404, 'User not found')

        if Address.get_by_id(args['address_id']) is None:
            abort(404, 'Address not found')

        if Cleaner.get_by_id(args['cleaner_id']) is None:
            abort(404, 'Cleaner not found')

        # Create new order
        order = Order(user_id=user_id, address_id=args['address_id'], cleaner_id=args['cleaner_id'], date=args['date'],
                        start_time=args['start_time'], end_time=args['end_time'], rooms=args['rooms'],
                        special_rooms=args['special_rooms'], extra_services=args['extra_services'], reference=args['reference'],
                        transaction=args['transaction'], price=args['price']
                      )

        # Persist and return order
        success = order.persist()
        if not success:
            abort(400, 'Parameters incorrect')

        return order, 201


class OrderListByCleanerAPI(Resource):
    """
    Resource to manage cleaner's order list
    """

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self, cleaner_id):
        # Return all cleaner's orders
        return Order.get_all_by_cleaner(cleaner_id)


class OrderListByAddressAPI(Resource):
    """
    Resource to manage user addresses list
    """

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self, address_id):
        # Return all orders by address
        return Order.get_all_by_address(address_id)
