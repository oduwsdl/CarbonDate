import pytest
import os
# import modules.cdGetGoogle as google
# import modules.cdGetBitly as bitly
import modules.cdGetBing as bing
import modules.cdGetTwitter as twitter


@pytest.mark.skip(reason='not implemented')
def test_Google():
    pass


@pytest.mark.skipif(os.getenv('CD_Bitly_token') is None,
                    reason="Missing Bitly key in environment")
def test_Bitly():
    pass


@pytest.mark.skipif(os.getenv('CD_Bing_key') is None,
                    reason="Missing Bing key in environment")
def test_Bing():
    testarry = ['']
    bing.getBing("", testarry, 0, verbose=False, displayArray={"Bing": ""})
    pass


@pytest.mark.parametrize("uri, memDate", [
    ("http://www.cs.odu.edu",
     "2008-12-01T03:53:27")
])
def test_Twitter(uri, memDate):
    testarry = ['']
    date = twitter.getTwitter(uri, testarry, 0, verbose=True,
                              displayArray={"Twitter": ""})
    assert memDate == date

# todo -- any external apis added should be tested here
