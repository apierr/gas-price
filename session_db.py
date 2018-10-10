#!/usr/bin/env python
from sqlalchemy import create_engine
from metadata_db import Base, Transaction
from sqlalchemy.orm import sessionmaker

def get_session_db(db_name = 'tx.db'):
    engine = create_engine('///'.join(['sqlite:', db_name]))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    return DBSession()
