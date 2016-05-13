from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.order import Order
from app.common.utils import assign

order_fields = {
    'date': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'rooms': fields.String,
    'special_rooms': fields.String,
    'extra_services': fields.String,
    # 'cleaner': fields.Url('cleaner', absolute=True),
    # 'address': fields.Url('address', absolute=True)
}

order_list_fields = {
    'date': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'rooms': fields.String,
    'special_rooms': fields.String,
    'extra_services': fields.String,
    'url': fields.Url('order', absolute=True)
}


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
        super(OrderAPI, self).__init__()

    @auth.login_required
    @marshal_with(order_fields, envelope='order')
    def get(self, id):
        # Get order by id
        order = Order.get_by_id(id)
        if order is None:
            abort(404)

        # Return order
        return order

    @auth.login_required
    @marshal_with(order_fields, envelope='order')
    def put(self, id):
        # Get order by id
        order = Order.get_by_id(id)
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

        # Persist changes and return order
        order.persist()
        return order

    @auth.login_required
    def delete(self, id):
        # Delete order
        success = Order.delete_by_id(id)
        if not success:
            abort(404)

        return {'result': True}


class OrderListAPI(Resource):
    """
    Resource to manage orders list
    """

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self):
        # Return all orders
        return Order.get_all()


class OrderListByUserAPI(Resource):
    """
    Resource to manage user orders list
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cleaner_id', type=str, required=True, help='No cleaner provided', location='json')
        self.parser.add_argument('address_id', type=str, required=True, help='No address provided', location='json')
        self.parser.add_argument('date', type=str, required=True, help='No date provided', location='json')
        self.parser.add_argument('start_time', type=str, required=True, help='No start time provided', location='json')
        self.parser.add_argument('end_time', type=str, required=True, help='No end time provided', location='json')
        self.parser.add_argument('rooms', type=str, required=True, help='No number of rooms provided', location='json')
        self.parser.add_argument('special_rooms', type=str, required=False, default=None, location='json')
        self.parser.add_argument('extra_services', type=str, required=False, default=None, location='json')
        super(OrderListByUserAPI, self).__init__()

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self, id):
        # Return all user's orders
        return Order.get_all_by_user(id)

    @auth.login_required
    @marshal_with(order_list_fields, envelope='order')
    def post(self, id):
        # Create new order
        args = self.parser.parse_args()
        order = Order(user_id=id, address_id=args['address_id'], cleaner_id=args['cleaner_id'], date=args['date'],
                        start_time=args['start_time'], end_time=args['end_time'], rooms=args['rooms'],
                        special_rooms=args['special_rooms'], extra_services=args['extra_services'])

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
    def get(self, id):
        # Return all cleaner's orders
        return Order.get_all_by_cleaner(id)


class OrderListByAddressAPI(Resource):
    """
    Resource to manage user addresses list
    """

    @auth.login_required
    @marshal_with(order_list_fields, envelope='orders')
    def get(self, id):
        # Return all orders by address
        return Order.get_all_by_address(id)
