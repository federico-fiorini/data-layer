from app import db


class Schedule(db.Model):
    """
    Model that maps 'schedule' table from the database
    """

    __tablename__ = 'schedule'

    schedule_id = db.Column(db.Integer, primary_key=True)
    cleaner_id = db.Column(db.Integer, db.ForeignKey('cleaner.cleaner_id'))
    year = db.Column(db.String(4), unique=False)
    week = db.Column(db.String(2), unique=False)
    day_of_week = db.Column(db.String(1), unique=False)
    start_time = db.Column(db.Time(), unique=False)
    end_time = db.Column(db.Time(), unique=False)

    def __init__(self, cleaner_id=None, year=None, week=None, day_of_week=None, start_time=None, end_time=None):
        self.cleaner_id = cleaner_id
        self.year = year
        self.week = week
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Schedule %r>' % self.schedule_id

    def persist(self):
        db.session.add(self)
        db.session.commit()
        self.cleaner_id

    @staticmethod
    def get_all(filter_dict):

        query = db.session.query(Schedule)
        for attr, value in filter_dict.items():
            query = query.filter(getattr(Schedule, attr).like("%%%s%%" % value))

        return query.all()

    @staticmethod
    def get_all_by_cleaner(cleaner_id, filter_dict):

        query = db.session.query(Schedule)
        for attr, value in filter_dict.items():
            query = query.filter(getattr(Schedule, attr).like("%%%s%%" % value))

        return query.filter_by(cleaner_id=cleaner_id).all()

    @staticmethod
    def get_by_id(schedule_id):
        return Schedule.query.filter_by(schedule_id=schedule_id).first()

    @staticmethod
    def delete_by_id(schedule_id):
        schedule = Schedule.query.filter_by(schedule_id=schedule_id).first()
        if schedule is None:
            return False

        db.session.delete(schedule)
        db.session.commit()
        return True

