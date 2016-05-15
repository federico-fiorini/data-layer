from app import db
from sqlalchemy.exc import IntegrityError


class Order(db.Model):
    """
    Model that maps 'order' table from the database
    """

    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    cleaner_id = db.Column(db.Integer, db.ForeignKey('cleaner.cleaner_id'))
    date = db.Column(db.Date(), unique=False)
    start_time = db.Column(db.Time(), unique=False)
    end_time = db.Column(db.Time(), unique=False)
    rooms = db.Column(db.Integer(), unique=False)
    special_rooms = db.Column(db.String(500), unique=False)
    extra_services = db.Column(db.String(500), unique=False)

    def __init__(self, user_id=None, address_id=None, cleaner_id=None, date=None, start_time=None, end_time=None, rooms=None, special_rooms=None, extra_services=None):
        self.user_id = user_id
        self.address_id = address_id
        self.cleaner_id = cleaner_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.rooms = rooms
        self.special_rooms = special_rooms
        self.extra_services = extra_services

    def __repr__(self):
        return '<Order %r>' % self.order_id

    def persist(self):
        try:
            db.session.add(self)
            db.session.commit()
            self.user_id
            self.address_id
            self.cleaner_id
        except IntegrityError:
            return False

        return True

    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def get_all_by_user(user_id):
        return Order.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_by_cleaner(cleaner_id):
        return Order.query.filter_by(cleaner_id=cleaner_id).all()

    @staticmethod
    def get_all_by_address(address_id):
        return Order.query.filter_by(address_id=address_id).all()

    @staticmethod
    def get_by_id(order_id):
        return Order.query.filter_by(order_id=order_id).first()

    @staticmethod
    def delete_by_id(order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        if order is None:
            return False

        db.session.delete(order)
        db.session.commit()
        return True

