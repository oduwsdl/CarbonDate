import modules.cdGetLowest as cd


def test_validateDate():
    '''
    Alters date to last second of the day
    '''
    validatedDate = cd.validateDate("")
    assert validatedDate == ""
    validatedDate = cd.validateDate("2017-07-04T00:00:00")
    assert validatedDate == "2017-07-04T23:59:59"


def test_getLowest():
    '''
    Get earliest date from an array. Nothing before 1995-01-01T12:00:00
    has been publicly archived.
    '''
    dates = ["2017-07-04T00:00:01",
             "2017-04-07T06:06:05",
             "1994-12-20T12:12:34",
             "2016-09-01T06:07:04",
             ]
    earliest = cd.getLowest(dates)
    assert earliest == "2016-09-01T06:07:04"
    dates = []
    earliest = cd.getLowest(dates)
    assert earliest == ""


def test_getLowestSources():
    '''
    Get earliest date and sources from sources dictionary with each key
    having a dictionary with the key 'earliest'
    '''
    sources = {
        "some.archive.com": {
            "earliest": "2016-09-01T06:07:04"
        },
        "is.archive.com": {
            "earliest": "2017-04-07T06:06:05"
        },
        "archiving.org": {
            "earliest": "2016-09-01T06:07:04"
        },
    }
    earliest_date, earliest_sources = cd.getLowestSources(sources)
    assert earliest_date == "2016-09-01T06:07:04"
    assert "archiving.org" in earliest_sources and \
        "some.archive.com" in earliest_sources

    sources = {}
    earliest_date, earliest_sources = cd.getLowestSources(sources)
    assert earliest_date == ""
    assert len(earliest_sources) == 0
