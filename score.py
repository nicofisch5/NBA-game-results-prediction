from init import Base
from sqlalchemy import Column, Integer, String, Enum


class Score(Base):
    __tablename__ = 'score'

    game_id = Column(Integer, primary_key=True)
    period = Column(String(10), primary_key=True)
    ha = Column(Enum('H', 'A'), primary_key=True)
    score = Column(Integer)
