import constants
import os
from sqlalchemy import create_engine, MetaData

__all__ = ["engine", "metadata"]

connect_string = 'sqlite:///' + os.path.join(constants.ROOT_PATH, 'db.sqlite')
engine = create_engine(connect_string, echo=True, encoding='UTF-8', convert_unicode=True)
metadata = MetaData(engine)
