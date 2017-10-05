from init import Base
from sqlalchemy import Column, Integer, String, Date, Enum


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    code = Column(String(20))
    season = Column(String(12))
    date = Column(Date)
    time = Column(String(45))
    type = Column(String(20))
    dce = Column(Enum('D', 'C', 'E'))
    winner = Column(Enum('H', 'A'))
