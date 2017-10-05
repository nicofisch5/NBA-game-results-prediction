from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://ml:ml99__NBA+-*@localhost:3306/NBA-games', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
Base.metadata.bind = engine