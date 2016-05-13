from app import db


class Service(db.Model):
    """
    Model that maps 'service' table from the database
    """

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('normal', 'special', 'extra'), unique=False)
    name = db.Column(db.String(50), unique=False)
    time = db.Column(db.Interval(), unique=False)

    def __init__(self, type=None, name=None, time=None):
        self.type = type
        self.name = name
        self.time = time

    def __repr__(self):
        return '<Service %r>' % self.id

    def persist(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Service.query.all()

    @staticmethod
    def get_by_id(service_id):
        return Service.query.filter_by(id=service_id).first()

    @staticmethod
    def delete_by_id(service_id):
        service = Service.query.filter_by(id=service_id).first()
        if service is None:
            return False

        db.session.delete(service)
        db.session.commit()
        return True
