from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy url format : driver://user:pass@host/database
# sqlite://<nohostname>/<path>(default : relative)
engine = create_engine('sqlite:///mydb.db', convert_unicode=True, poolclass=NullPool)
# NullPool => db_session.close() will automatically do same jobs engine.dispose() do.
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  import models
  Base.metadata.create_all(engine)

