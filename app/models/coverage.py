from app import db


class Coverage(db.Model):
    """
    Model that maps 'cleaner_coverage' table from the database
    """

    __tablename__ = 'coverage'
    cleaner_id = db.Column(db.Integer, db.ForeignKey('cleaner.cleaner_id'), primary_key=True)
    zip = db.Column(db.Integer, unique=False, primary_key=True)

    def __init__(self, cleaner_id=None, zip=None):
        self.cleaner_id = cleaner_id
        self.zip = zip

    def __repr__(self):
        return '<Coverage %r %r>' % self.cleaner_id, self.zip

    def persist(self):
        db.session.add(self)
        db.session.commit()
        self.cleaner_id

    @staticmethod
    def get_all():
        return Coverage.query.all()

    @staticmethod
    def get_by_cleaner_and_zip(cleaner_id, zip):
        return Coverage.query.filter_by(cleaner_id=cleaner_id, zip=zip).first()

    @staticmethod
    def get_all_by_cleaner(cleaner_id):
        return Coverage.query.filter_by(cleaner_id=cleaner_id).all()

    @staticmethod
    def get_all_by_zip(zip):
        return Coverage.query.filter_by(zip=zip).all()

    @staticmethod
    def delete_by_cleaner_zip(cleaner_id, zip):
        coverage = Coverage.query.filter_by(cleaner_id=cleaner_id, zip=zip).first()
        if coverage is None:
            return False

        db.session.delete(coverage)
        db.session.commit()
        return True

