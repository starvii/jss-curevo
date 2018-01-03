import time
from method import idgen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, INTEGER, VARCHAR, CHAR, TEXT, Index
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker


__connect_string = 'sqlite:///:memory:'

Base = declarative_base()
engine = create_engine(__connect_string, echo=True, encoding='UTF-8', convert_unicode=True)
metadata = MetaData(engine)

session_data = Table('session_data', metadata,
                     Column('id', CHAR(40), primary_key=True),
                     Column('k', VARCHAR(255), primary_key=True),
                     Column('v', TEXT),
                     Column('timestamp', INTEGER),
                     Column('timeout', INTEGER),
                     Index('idx', 'id', 'k', unique=True),
                     )

metadata.create_all(bind=engine)

__auto_map_base = automap_base(metadata=metadata)
__auto_map_base.prepare()
SessionData = __auto_map_base.classes.session_data


class SessionBackEnd(object):
    def __init__(self):
        self.__db = scoped_session(sessionmaker(bind=engine))

    def get_value(self, session_id, key):
        value = self.__db.query(SessionData.value).filter_by(id=session_id, k=key).first()
        return value

    def set_value(self, session_id, key, value, timeout=1800):
        sd = SessionData(id=session_id, k=key, v=value, timestamp=int(time.time()), timeout=timeout)
        self.__db.merge(sd)
        self.__db.flush()

    def delete_value(self, session_id, key):
        self.__db.query(SessionData).filter_by(id=session_id, k=key).delete()

    def clear_session(self, session_id):
        self.__db.query(SessionData).filter_by(id=session_id).delete()

    def cleanup_session(self):
        now = int(time.time())
        self.__db.query(SessionData).filter((now - SessionData.timestamp) > SessionData.timeout).delete()


class HttpSession(object):
    def __init__(self, session_id, session_back_end):
        self.__session_id = session_id
        self.__session_back_end = session_back_end

    def get_value(self, key):
        return self.__session_back_end.get_value(self.__session_id, key)

    def set_value(self, key, value, timeout=1800):
        self.__session_back_end.set_value(self.__session_id, key, value, timeout)

    def delete_value(self, key):
        self.__session_back_end.delete_value(self.__session_id, key)

    def clear_session(self):
        self.__session_back_end.clear_session(self.__session_id)


def session(request):
    def process(handler, *args, **kwargs):
        session_id = handler.get_secure_cookie('session_id', '')
        if not session_id or len(session_id.strip()) == 0:
            # create session
            session_id = idgen.create_session_id()
            # handler.application.backend.set_session(session_id, '', None)
            handler.set_secure_cookie('session_id', session_id, secure=True, httponly=True)
        if not hasattr(handler, 'http_session'):
            setattr(handler, 'http_session', HttpSession(session_id, handler.application.backend))
        request(handler, *args, **kwargs)
        # TODO: clear the timeout sessions
    return process
