from init import Base
from sqlalchemy import Column, Integer, String


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    code = Column(String(20))
    name = Column(String(100))
    division = Column(String(45))
    conference = Column(String(15))
