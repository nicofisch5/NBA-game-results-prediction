from init import Base
from sqlalchemy import Column, ForeignKey, Integer, Float, Enum


class TeamStat(Base):
    __tablename__ = 'team_stat'

    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    ha = Column(Enum('H', 'A'), primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    result = Column(Enum('W', 'L'))
    STLP = Column(Float)
    FT = Column(Integer)
    b2PA = Column(Integer)
    FG = Column(Integer)
    DRB = Column(Integer)
    ORBP = Column(Float)
    AST = Column(Integer)
    b3PAr = Column(Float)
    PF = Column(Integer)
    FGA = Column(Integer)
    DRBr = Column(Float)
    b2P = Column(Integer)
    ORBr = Column(Float)
    TOVP = Column(Float)
    ASTP = Column(Float)
    FTAr = Column(Float)
    FIC = Column(Float)
    eFGP = Column(Float)
    FGP = Column(Float)
    b2PAr = Column(Float)
    PlusMinus = Column(Integer)
    USGP = Column(Float)
    DRtg = Column(Float)
    b2PP = Column(Float)
    DRBP = Column(Float)
    ORtg = Column(Float)
    TRBP = Column(Float)
    ORB = Column(Integer)
    b3P = Column(Integer)
    TOV = Column(Integer)
    STLonTOV = Column(Float)
    TSA = Column(Float)
    ASTonTOV = Column(Float)
    b3PA = Column(Integer)
    BLKP = Column(Float)
    FTP = Column(Float)
    PTS = Column(Integer)
    HOB = Column(Float)
    STL = Column(Integer)
    TRB = Column(Integer)
    FTA = Column(Integer)
    BLK = Column(Integer)
    FTr = Column(Float)
    TSP = Column(Float)
    FTonFGA = Column(Float)
    b3PP = Column(Float)