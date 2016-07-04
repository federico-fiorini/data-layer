from app import db
from sqlalchemy.exc import IntegrityError

class PotentialUser(db.Model):
    """
    Model that maps 'users' table from the database
    """

    __tablename__ = 'potential_user'

    potential_user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    zip = db.Column(db.String(10), unique=False)
    date = db.Column(db.Date(), unique=False)

    def __init__(self, email=None, zip=None, date=None):
        self.email = email
        self.zip = zip
        self.date = date

    def __repr__(self):
        return '<PotentialUser %r>' % self.user_id

    def persist(self):
        try:
            db.session.add(self)
            db.session.commit()
            self.potential_user_id
        except IntegrityError:
            return False

        return True

    @staticmethod
    def get_all():
        return PotentialUser.query.all()

    @staticmethod
    def get_by_id(potential_user_id):
        return PotentialUser.query.filter_by(potential_user_id=potential_user_id).first()

    @staticmethod
    def get_all_by_zip(zip):
        return PotentialUser.query.filter_by(zip=zip).all()

    @staticmethod
    def delete_by_id(potential_user_id):
        potential_user = PotentialUser.query.filter_by(potential_user_id=potential_user_id).first()
        if potential_user is None:
            return False

        db.session.delete(potential_user)
        db.session.commit()
        return True
