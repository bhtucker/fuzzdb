# -*- coding: utf-8 -*-
"""
    models.py
    ~~~~~~~~~

    database models for string clustering application
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///persist/strings.db', echo=True)
Base = declarative_base()


class Citation(Base):

    __tablename__ = "citations"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    citation_date = Column(Date)
    citation_id = Column(String)

    def __init__(self, **kwargs):

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
