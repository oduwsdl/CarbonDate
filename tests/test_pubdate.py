import pytest
import modules.cdGetPubdate as pub


@pytest.mark.parametrize("uri", [
    ("http://www.cnn.com/2012/10/28/world/americas"
     "/canada-earthquake/index.html"),
    ("http://www.cnn.com/2011/10/28/living/ways-to-look-better-is/index.html"),
])
def test_pubdate(uri):
    '''Main method of pubdate module. '''
    date = pub.getPubdate(uri, [''], 0, verbose=False,
                          displayArray={"Pubdate": ""})
    print(date)
    assert len(date) > 0


def test_parseStrDate():
    ''' '''
    date = pub.parseStrDate("2002-08-12T00:00:50")
    assert date.year == 2002
    assert date.month == 8
    assert date.day == 12
    assert date.second == 50

    date = pub.parseStrDate("notapropperdate")
    assert date is None


def test_extractFromURL():
    '''Retrieves datetime object from URL '''
    uri = ("http://www.cnn.com/2011/10/28/living/ways-to-look-better-is"
           "/index.html")
    date = pub._extractFromURL(uri)
    assert date.year == 2011
    assert date.month == 10
    assert date.day == 28

    uri = ("http://www.cs.odu.edu")
    date = pub._extractFromURL(uri)
    assert date is None


def test_notAliveWebsite():
    '''Check if a 404 website with an article date still retrieves a date'''
    uri = ("http://notalivenewssite.com/2015/11/15/news.html")
    date = pub.getPubdate(uri, [''], 0, verbose=False,
                          displayArray={"Pubdate": ""})
    assert len(date) > 0
    uri = ("http://notalivenewssite.com/news.html")
    date = pub.getPubdate(uri, [''], 0, verbose=False,
                          displayArray={"Pubdate": ""})
    assert len(date) == 0
