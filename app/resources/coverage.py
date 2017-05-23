from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.coverage import Coverage
from app.models.cleaner import Cleaner

coverage_fields = {
    'cleaner': fields.Url('cleaner', absolute=False),
    'zip': fields.Integer
}

coverage_list_fields = coverage_fields.copy()
coverage_list_fields['url'] = fields.Url('cleaner_coverage', absolute=False)


class CoverageAPI(Resource):
    """
    Resource to manage cleaner individual coverage
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('zip', type=int, required=True, location='json')
        super(CoverageAPI, self).__init__()

    @auth.login_required
    @marshal_with(coverage_fields, envelope='coverage')
    def get(self, cleaner_id, zip):
        # Get unique coverage by cleaner and zip
        coverage = Coverage.get_by_cleaner_and_zip(cleaner_id, zip)
        if coverage is None:
            abort(404)

        # Return user
        return coverage

    @auth.login_required
    def delete(self, cleaner_id, zip):
        # Delete schedule
        success = Coverage.delete_by_cleaner_zip(cleaner_id, zip)
        if not success:
            abort(404)

        return {'result': True}


class CoverageListAPI(Resource):
    """
    Resource to manage coverage list
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cleaner_id', type=int, required=False, location='args')
        self.parser.add_argument('zip', type=int, required=False, location='args')
        super(CoverageListAPI, self).__init__()

    @auth.login_required
    @marshal_with(coverage_list_fields, envelope='coverages')
    def get(self):
        # Return all coverages
        return Coverage.get_all()


class CoverageListByCleanerAPI(Resource):
    """
    Resource to manage cleaner schedules list
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('zip', type=int, required=True, help='No zip code provided', location='json')
        super(CoverageListByCleanerAPI, self).__init__()

    @auth.login_required
    @marshal_with(coverage_list_fields, envelope='coverage')
    def get(self, cleaner_id):
        return Coverage.get_all_by_cleaner(cleaner_id)

    @auth.login_required
    @marshal_with(coverage_list_fields, envelope='coverage')
    def post(self, cleaner_id):

        # Validate cleaner
        if Cleaner.get_by_id(cleaner_id) is None:
            abort(404, 'Cleaner not found')

        args = self.parser.parse_args()
        coverage = Coverage(cleaner_id=cleaner_id,  zip=args['zip'])

        # Persist and return schedule
        try:
            coverage.persist()
        except:
            abort(500, 'Zip already inserted')

        return coverage, 201


class CoverageListByZipAPI(Resource):
    @auth.login_required
    @marshal_with(coverage_list_fields, envelope='coverages')
    def get(self, zip):
        return Coverage.get_all_by_zip(zip)
