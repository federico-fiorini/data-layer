from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.cleaner import Cleaner
from app.common.utils import assign

cleaner_fields = {
    'name': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'mobile_number': fields.String,
    'description': fields.String,
    'review_rate': fields.String,
    'last_review': fields.String,
    'picture_url': fields.String,
    'schedules': fields.Url('cleaner_schedule', absolute=False),
    'orders': fields.Url('cleaner_orders', absolute=False)
}

cleaner_list_fields = {
    'name': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'mobile_number': fields.String,
    'description': fields.String,
    'review_rate': fields.String,
    'last_review': fields.String,
    'picture_url': fields.String,
    'schedules': fields.Url('cleaner_schedule', absolute=False),
    'orders': fields.Url('cleaner_orders', absolute=False),
    'url': fields.Url('cleaner', absolute=False)
}


class CleanerListAPI(Resource):
    """
    Resource to manage cleaners
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='No name provided', location='json')
        self.parser.add_argument('lastname', type=str, required=True, help='No last name provided', location='json')
        self.parser.add_argument('email', type=str, default="", location='json')
        self.parser.add_argument('mobile_number', type=str, required=True, help='No mobile number provided', location='json')
        self.parser.add_argument('description', type=str, default=None, location='json')
        self.parser.add_argument('review_rate', type=str, default=None, location='json')
        self.parser.add_argument('last_review', type=str, default=None, location='json')
        self.parser.add_argument('picture_url', type=str, default=None, location='json')
        super(CleanerListAPI, self).__init__()

    @auth.login_required
    @marshal_with(cleaner_list_fields, envelope='cleaners')
    def get(self):
        # Return all cleaners
        return Cleaner.get_all()

    @auth.login_required
    @marshal_with(cleaner_list_fields, envelope='cleaner')
    def post(self):
        # Create new cleaner
        args = self.parser.parse_args()
        cleaner = Cleaner(name=args['name'], lastname=args['lastname'], email=args['email'],
                          mobile_number=args['mobile_number'], description=args['description'],
                          review_rate=args['review_rate'], last_review=args['last_review'],
                          picture_url=args['picture_url'])

        # Persist and return cleaner
        success = cleaner.persist()
        if not success:
            abort(400, "Cleaner already exists")

        return cleaner, 201


class CleanerAPI(Resource):
    """
    Resource to manage individual cleaner
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('lastname', type=str, location='json')
        self.parser.add_argument('email', type=str, location='json')
        self.parser.add_argument('mobile_number', type=str, location='json')
        self.parser.add_argument('description', type=str, location='json')
        self.parser.add_argument('review_rate', type=str, location='json')
        self.parser.add_argument('last_review', type=str, location='json')
        self.parser.add_argument('picture_url', type=str, location='json')
        super(CleanerAPI, self).__init__()

    @auth.login_required
    @marshal_with(cleaner_fields, envelope='cleaner')
    def get(self, cleaner_id):
        # Get cleaner by id
        cleaner = Cleaner.get_by_id(cleaner_id)
        if cleaner is None:
            abort(404)

        # Return cleaner
        return cleaner

    @auth.login_required
    @marshal_with(cleaner_fields, envelope='cleaner')
    def put(self, cleaner_id):
        # Get cleaner by id
        cleaner = Cleaner.get_by_id(cleaner_id)
        if cleaner is None:
            abort(404)

        # Update cleaner fields
        args = self.parser.parse_args()
        cleaner.name = assign(args['name'], cleaner.name)
        cleaner.lastname = assign(args['lastname'], cleaner.lastname)
        cleaner.email = assign(args['email'], cleaner.email)
        cleaner.mobile_number = assign(args['mobile_number'], cleaner.mobile_number)
        cleaner.description = assign(args['description'], cleaner.description)
        cleaner.review_rate = assign(args['review_rate'], cleaner.review_rate)
        cleaner.last_review = assign(args['last_review'], cleaner.last_review)
        cleaner.picture_url = assign(args['picture_url'], cleaner.picture_url)

        # Persist changes and return cleaner
        cleaner.persist()
        return cleaner

    @auth.login_required
    def delete(self, cleaner_id):
        # Delete cleaner
        success = Cleaner.delete_by_id(cleaner_id)
        if not success:
            abort(404)

        return {'result': True}
