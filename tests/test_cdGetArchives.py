import pytest
import time
import calendar
import modules.cdGetArchives as m
import json


def dateToEpoch(date):
    epoch = int(calendar.timegm(time.strptime(
        date, '%Y-%m-%dT%H:%M:%S')))
    return epoch


@pytest.mark.parametrize("uri", [
    ("http://www.cs.odu.edu"),
    ("http://example.org"),
])
def test_numUniqueMementos(uri):
    '''Number of unique mementos. Dependent on Memgator API'''
    memento_list = m.getMementos(uri)
    assert len(memento_list) > 0
    for i in memento_list:
        for key, value in i.items():
            # for each dictionary key there should be some value.
            assert value


@pytest.mark.parametrize("uri, memDate", [
    ("http://web.archive.org/web/19970102130137/http://cs.odu.edu:80/",
     "1996-02-09T21:47:46"),
    ("http://arquivo.pt/wayback/20091223043049/http://www.cs.odu.edu/",
     "2009-12-23T04:30:50"),
])
def test_getRealDate(uri, memDate):
    '''Check if last modified date lower than found date'''
    realDate = m.getRealDate(uri, dateToEpoch(memDate))
    assert realDate == memDate


@pytest.mark.parametrize("uri", [
    ("http://www.cs.odu.edu"),
    ("http://www.cnn.com/2012/10/28/world/americas"
     "/canada-earthquake/index.html"),
])
def testGetArchives(uri):
    '''
    Calls getMementos and getRealDate to form a json dictionary.
    '''
    js = m.getArchives(uri, [''], 0, verbose=True,
                       displayArray={"": ""})
    # Check for non-nil value from each key
    assert len(js["Earliest"]) > 0
    print(json.dumps(js, sort_keys=True, indent=4))
    print()
    assert len(js["By_Archive"]) > 0
