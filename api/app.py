#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import Application
from sqlalchemy.orm import scoped_session, sessionmaker
from model import engine
from urls import urls
from method.session import SessionBackEnd

settings = dict(
    debug=True,
    cookie_secret='z1vHmmr97uuGfG5IJ5J33C4qV-_qVVnx',
)

app = Application(handlers=urls, **settings)
app.db = scoped_session(sessionmaker(bind=engine))
app.backend = SessionBackEnd()
