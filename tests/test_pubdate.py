import pytest
import modules.cdGetPubdate as pub


@pytest.mark.skip(reason='not implemented')
def test_pubdate():
    testarry = ['']
    pub.getPubdate("", testarry, 0, verbose=False,
                   displayArray={"Pubdate": ""})
    pass
