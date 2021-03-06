import configobj
import os.path
import pydrugshortagesca 
import pytest

CONFIG_PATH=os.path.expanduser('~/.config/pydrugshortagesca/config')
@pytest.fixture
def session(): 
    if os.path.exists(CONFIG_PATH):
        config = configobj.ConfigObj(CONFIG_PATH)
        email, password = config['email'], config['password']
    else: 
        pytest.exit("config file not found at {}".format(CONFIG_PATH))
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

def test_isearch_filter_all(session):
    session.login()
    import itertools
    results = list(itertools.islice(session.isearch(_filter=lambda x: False,term='venlafaxine'), 10))
    assert len(results) == 0

def test_shortage_report(session):
    session.login()

    report_id = '95366'  # cyanocobalamin 2019-12-17
    results = session.shortage_report(report_id)
    assert "drug" in results

def test_discontinuation_report(session):
    session.login()

    report_id = '60563' 
    results = session.discontinuation_report(report_id)
    assert "drug" in results

