# -*- coding: utf-8 -*-
"""
    fetch.py
    ~~~~~~~~

    get stuff
"""

import requests
from models import Citation, engine
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse as dateparse


def check_db_for_citations(session):
    citations = session.query(Citation).limit(2).all()
    if (all([x for x in citations]) and citations):
        return True
    else:
        return False


def get_web_citations():
    url = "https://data.cityofnewyork.us/resource/f6cc-a2kg.json"
    rows = []
    for i in range(0, 10000, 1000):
        params = {
            "$limit": 1000,
            "$offset": i,
            "$select": "ticket_number,violation_date,respondent_first_name,respondent_last_name"
        }
        r = requests.get(url, params=params)
        rows += r.json()
    return rows


def store_citations(session, citations):
    for row in citations:
        vdate = dateparse(
            row.get('violation_date')
        ).date() if 'violation_date' in row else None

        citation_kwargs = {
            'first_name': row.get('respondent_first_name'),
            'last_name': row.get('respondent_last_name'),
            'citation_date': vdate,
            'citation_id': row.get('ticket_number')
        }

        session.add(Citation(**citation_kwargs))

    session.commit()


def make_session():
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    return session


def ensure_citations():

    session = make_session()
    have_citations = check_db_for_citations(session)

    if not have_citations:
        store_citations(session, get_web_citations())

    session.rollback()


def get_local_citations(session=None, ensure=True):
    if ensure:
        ensure_citations()
    session = session or make_session()

    return session.query(Citation).all()
