from app import db
from sqlalchemy.exc import IntegrityError


class Cleaner(db.Model):
    """
    Model that maps 'cleaner' table from the database
    """

    __tablename__ = 'cleaner'

    cleaner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    lastname = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    mobile_number = db.Column(db.String(15), unique=True)
    description = db.Column(db.String(500), unique=False)
    review_rate = db.Column(db.Numeric, unique=False)
    last_review = db.Column(db.String(500), unique=False)
    orders = db.relationship('Order', backref='cleaner', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='cleaner', lazy='dynamic')

    def __init__(self, name=None, lastname=None, email=None, mobile_number=None, description=None, review_rate=None,
                 last_review=None):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.mobile_number = mobile_number
        self.description = description
        self.review_rate = review_rate
        self.last_review = last_review

    def __repr__(self):
        return '<Cleaner %r>' % self.cleaner_id

    def persist(self):
        try:
            db.session.add(self)
            db.session.commit()
            self.cleaner_id
        except IntegrityError:
            return False

        return True

    @staticmethod
    def get_all():
        return Cleaner.query.all()

    @staticmethod
    def get_by_id(cleaner_id):
        return Cleaner.query.filter_by(cleaner_id=cleaner_id).first()

    @staticmethod
    def delete_by_id(cleaner_id):
        cleaner = Cleaner.query.filter_by(cleaner_id=cleaner_id).first()
        if cleaner is None:
            return False

        db.session.delete(cleaner)
        db.session.commit()
        return True
