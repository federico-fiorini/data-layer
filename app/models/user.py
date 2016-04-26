from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    last_name = Column(String(50), unique=False)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, last_name=None, email=None):
        self.name = name
        self.email = email
        self.last_name = last_name

    def __repr__(self):
        return '<User %r>' % self.name
