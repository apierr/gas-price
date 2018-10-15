#!/usr/bin/env python
from sqlalchemy import create_engine
from metadata_db import Base, Transaction
from sqlalchemy.orm import sessionmaker
import config as cfg

def get_session_db():
    engine = create_engine(cfg.db_url)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    return DBSession()
