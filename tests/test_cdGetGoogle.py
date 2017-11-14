import pytest
import os
import modules.cdGetGoogle as g


@pytest.fixture
def page():
    # use samples to not prod google
    pagePath = os.path.join(os.path.dirname(__file__) +
                            "/samples/google/spans-only.html")
    page = open(pagePath).read()
    return page


def test_getGoogle():
    url = "http://www.cs.odu.edu"
    earliest = g.getGoogle(url, [''], 0, verbose=False,
                           displayArray={"Google": ""})
    assert len(earliest) > 0


def test_findSignatures(page):
    positions = g.findSignatures(page)
    assert len(positions) > 0


def test_findCreationDate(page):
    date = g.genericGetCreationDate(page)
    assert len(date) > 0
