import pydrugshortagesca 
import pytest

@pytest.fixture
def session(): 
    import os.path
    if os.path.exists(".api"):
        email, password = open(".api").read().split()
    else: 
        email, password = None, None
    return pydrugshortagesca.Session(email, password)

def test_login(session):
    session.login()

def test_search_no_login(session):
    with pytest.raises(pydrugshortagesca.NotLoggedInException):
        session.search()

def test_isearch_no_login(session):
    with pytest.raises(pydrugshortagesca.NotLoggedInException):
        list(session.isearch())

def test_shortage_no_login(session):
    with pytest.raises(pydrugshortagesca.NotLoggedInException):
        session.shortage_report("0")

def test_discontinuation_no_login(session):
    with pytest.raises(pydrugshortagesca.NotLoggedInException):
        session.discontinuation_report("0")

def test_search_all(session):
    session.login()

    results = session.search()
    assert results['total'] > 0

def test_isearch_all(session):
    session.login()
    import itertools
    results = list(itertools.islice(session.isearch(), 10))
    assert len(results) == 10

def test_shortage_report(session):
    session.login()

    report_id = '95366'  # cyanocobalamin 2019-12-17
    results = session.shortage_report(report_id)
    assert "drug" in results
