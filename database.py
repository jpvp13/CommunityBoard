from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

engine = create_engine('sqlite:///alternative.db', echo = True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False, bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind = engine)
    # session = Session()
    

