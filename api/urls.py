#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
the url structure of website
"""

from tornado.web import URLSpec
from tornado.web import StaticFileHandler
from handler.teacher import url as teacher_url
from handler.natural_class import url as natural_class_url
from handler.teaching_class import url as teaching_class_url
import constants
import os

STATIC_PATH = os.path.join(os.path.dirname(__file__), os.path.join(constants.ROOT_PATH, '../web/dist'))
static_handler = URLSpec(r'/(.*)', StaticFileHandler, {'path': STATIC_PATH, 'default_filename': 'index.html'})

urls = list()
urls.extend(teacher_url)
urls.extend(natural_class_url)
urls.extend(teaching_class_url)
urls.append(static_handler)
