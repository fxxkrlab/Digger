from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib import parse

from modules import load

db = load._cfg["database"]

db_string = db["connect"]
db_user = parse.quote_plus(f"{db['user']}")
db_passwd = parse.quote_plus(f"{db['passwd']}")
db_host = db["host"]
db_port = db["port"]
db_database = db["db"]

DB_URI = "{}://{}:{}@{}:{}/{}".format(
    db_string, db_user, db_passwd, db_host, db_port, db_database
)


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
