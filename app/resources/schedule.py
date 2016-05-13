from app.resources import auth
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
from app.models.schedule import Schedule
from app.common.utils import assign
from datetime import date

schedule_fields = {
    'year': fields.String,
    'week': fields.String,
    'day_of_week': fields.String,
    'start_time': fields.String,
    'end_time': fields.String
}

schedule_list_fields = {
    'year': fields.String,
    'week': fields.String,
    'day_of_week': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'url': fields.Url('schedule', absolute=True)
}


class ScheduleAPI(Resource):
    """
    Resource to manage cleaner individual schedule
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('year', type=str, required=False, location='json')
        self.parser.add_argument('week', type=str, required=False, location='json')
        self.parser.add_argument('day_of_week', type=str,  required=False, location='json')
        self.parser.add_argument('start_time', type=str,  required=False, location='json')
        self.parser.add_argument('end_time', type=str,  required=False, location='json')
        super(ScheduleAPI, self).__init__()

    @auth.login_required
    @marshal_with(schedule_fields, envelope='schedule')
    def get(self, id):
        # Get schedule by id
        schedule = Schedule.get_by_id(id)
        if schedule is None:
            abort(404)

        # Return user
        return schedule

    @auth.login_required
    @marshal_with(schedule_fields, envelope='schedule')
    def put(self, id):
        # Get schedule by id
        schedule = Schedule.get_by_id(id)
        if schedule is None:
            abort(404)

        # Update schedule fields
        args = self.parser.parse_args()
        schedule.year = assign(args['year'], schedule.year)
        schedule.week = assign(args['week'], schedule.week)
        schedule.day_of_week = assign(args['day_of_week'], schedule.day_of_week)
        schedule.start_time = assign(args['start_time'], schedule.start_time)
        schedule.end_time = assign(args['end_time'], schedule.end_time)

        # Persist changes and return schedule
        schedule.persist()
        return schedule

    @auth.login_required
    def delete(self, id):
        # Delete schedule
        success = Schedule.delete_by_id(id)
        if not success:
            abort(404)

        return {'result': True}


class ScheduleListAPI(Resource):
    """
    Resource to manage cleaner schedules list
    """

    @auth.login_required
    @marshal_with(schedule_list_fields, envelope='schedules')
    def get(self):
        # Return all user's schedules
        return Schedule.get_all()


class SheduleListByCleanerAPI(Resource):
    """
    Resource to manage cleaner schedules list
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('year', type=str, required=False, default='', location='json')
        self.parser.add_argument('week', type=str, required=True, help='No week number provided', location='json')
        self.parser.add_argument('day_of_week', type=str, required=True, help='No day of week provided', location='json')
        self.parser.add_argument('start_time', type=str, required=True, help='No start time provided', location='json')
        self.parser.add_argument('end_time', type=str, required=True, help='No end time provided', location='json')
        super(SheduleListByCleanerAPI, self).__init__()

    @auth.login_required
    @marshal_with(schedule_list_fields, envelope='schedules')
    def get(self, id):
        # Return all user's schedules
        return Schedule.get_all_by_cleaner(id)

    @auth.login_required
    @marshal_with(schedule_list_fields, envelope='schedule')
    def post(self, id):
        # Create new schedule
        args = self.parser.parse_args()
        if args['year'] == '':
            args['year'] = date.today().year

        schedule = Schedule(id, year=args['year'], week=args['week'], day_of_week=args['day_of_week'], start_time=args['start_time'], end_time=args['end_time'])

        # Persist and return schedule
        schedule.persist()
        return schedule, 201
