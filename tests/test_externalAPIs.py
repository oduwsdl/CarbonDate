import pytest
import os
# import modules.cdGetGoogle as google
import modules.cdGetBitly as bitly
import modules.cdGetBing as bing
import modules.cdGetTwitter as twitter


@pytest.mark.skip(reason='not implemented')
def test_Google():
    pass


@pytest.mark.skipif(os.getenv('CD_Bitly_token') is None,
                    reason="Missing Bitly key in environment")
def test_Bitly():
    url = "http://www.cs.odu.edu"
    date = bitly.getBitly(url, [''], 0, verbose=False,
                          displayArray={"bitly.com": ""})
    assert len(date) > 0


@pytest.mark.skipif(os.getenv('CD_Bitly_token') is None,
                    reason="Missing Bitly key in environment")
def test_BitlyJSON():
    url = "http://www.cs.odu.edu"
    apiURL = ('https://api-ssl.bitly.com/v3/link/lookup?'
              'access_token=ACCESS_TOKEN&url=' + url)
    bitlyJSON = bitly.GetBitlyJson(apiURL)
    assert bitlyJSON["status_code"] == 200

    # this shortened url should always remain the same or
    # Bitly's API will not allow reverse lookups
    assert bitlyJSON["data"]["link_lookup"][0]
    ["aggregate_link"] == "http://bit.ly/r9kIfC"


@pytest.mark.skipif(os.getenv('CD_Bing_key') is None,
                    reason="Missing Bing key in environment")
def test_Bing():
    testarry = ['']
    bing.getBing("", testarry, 0, verbose=False,
                 displayArray={"bing.com": ""})
    pass


@pytest.mark.parametrize("uri", [
    ("http://www.cs.odu.edu")
])
def test_Twitter(uri):
    testarry = ['']
    date = twitter.getTwitter(uri, testarry, 0, verbose=True,
                              displayArray={"twitter.com": ""})
    assert len(date) > 0

# todo -- any external apis added should be tested here
