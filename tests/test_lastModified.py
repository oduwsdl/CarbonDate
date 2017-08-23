import modules.cdGetLastModified as lastModified


def test_lastModified():
    ''' '''
    uri = "http://www.example.org/"
    lm = lastModified.getLastModified(uri, [''], 0, verbose=True,
                                      displayArray={"last-modified": ""})
    assert len(lm) > 0
    uri = "http://www.cs.odu.edu/"
    lm = lastModified.getLastModified(uri, [''], 0, verbose=True,
                                      displayArray={"last-modified": ""})
    assert len(lm) == 0
