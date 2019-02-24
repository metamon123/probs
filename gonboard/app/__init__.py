from flask import Flask
from flask_login import LoginManager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from custom_config import db_uri

# -- app --

app = Flask(__name__)
app.config.from_pyfile("../flask_config.py")


# -- login_manager --

login_manager = LoginManager(app)

# -- database --

engine = create_engine(db_uri, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()



# -- blueprint --

from .account.front import account_bp
app.register_blueprint(account_bp, url_prefix="/account")

# from .board.front import board_bp
# app.register_blueprint(board_bp)

def init_db():
  from .account import models
  # from board import models
  Base.metadata.create_all(engine)


@app.route("/")
def index():
    return "Not implemeted... Please visit /account"


@app.teardown_request
def remove_session(exception=None):
    db_session.remove()
