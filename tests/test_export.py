import pydrugshortagesca
import pytest

@pytest.fixture
def session(): 
    import os.path
    if os.path.exists(".api"):
        email, password = open(".api").read().split()
    else: 
        pytest.exit(".api credentials file not found")
    return pydrugshortagesca.Session(email, password)

def test_shortages_as_csv(session):
    session.login()

    import io
    output = io.StringIO()

    pydrugshortages.export.as_csv(session, output, report_id='60563')

    data = output.getvalue()
    assert len(data) > 0
