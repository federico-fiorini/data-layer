from app import db


class Address(db.Model):
    """
    Model that maps 'address' table from the database
    """

    __tablename__ = 'address'

    address_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    street = db.Column(db.String(50), unique=False)
    house_number = db.Column(db.String(10), unique=False)
    flat_number = db.Column(db.String(10), unique=False)
    post_code = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    country = db.Column(db.String(50), unique=False)
    neighbourhood = db.Column(db.String(50), unique=False)
    orders = db.relationship('Order', backref='address', lazy='dynamic')

    def __init__(self, user_id=None, street=None, house_number=None, flat_number=None, post_code=None, city=None,
                 country=None, neighbourhood=None):
        self.user_id = user_id
        self.street = street
        self.house_number = house_number
        self.flat_number = flat_number
        self.post_code = post_code
        self.city = city
        self.country = country
        self.neighbourhood = neighbourhood

    def __repr__(self):
        return '<Address %r>' % self.address_id

    def persist(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Address.query.all()

    @staticmethod
    def get_all_by_user(user_id):
        return Address.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(address_id):
        return Address.query.filter_by(address_id=address_id).first()

    @staticmethod
    def delete_by_id(address_id):
        address = Address.query.filter_by(address_id=address_id).first()
        if address is None:
            return False

        db.session.delete(address)
        db.session.commit()
        return True

