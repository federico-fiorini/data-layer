from app import db
from sqlalchemy.exc import IntegrityError

class User(db.Model):
    """
    Model that maps 'users' table from the database
    """

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    lastname = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    addresses = db.relationship('Address', backref='user', lazy='dynamic')
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def __init__(self, name=None, lastname=None, email=None):
        self.name = name
        self.email = email
        self.lastname = lastname

    def __repr__(self):
        return '<User %r>' % self.user_id

    def persist(self):
        try:
            db.session.add(self)
            db.session.commit()
            self.user_id
        except IntegrityError:
            return False

        return True

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def delete_by_id(user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            return False

        db.session.delete(user)
        db.session.commit()
        return True
