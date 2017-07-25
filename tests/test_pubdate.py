import pytest
import modules.cdGetPubdate as pub


@pytest.mark.parametrize("uri", [
    ("http://www.cnn.com/2012/10/28/world/americas"
     "/canada-earthquake/index.html"),
    ("http://www.cnn.com/2011/10/28/living/ways-to-look-better-is/index.html"),
])
def test_pubdate(uri):
    date = pub.getPubdate(uri, [''], 0, verbose=False,
                          displayArray={"Pubdate": ""})
    assert len(date) > 0
