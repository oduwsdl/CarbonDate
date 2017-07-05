import pytest
import modules.cdGetArchives as m


@pytest.mark.parametrize("uri, expectedCount", [
	("http://cs.odu.edu", 4),
	("http://example.org", 6),
])
def test_numUniqueMementos(uri,expectedCount):
	'''Number of unique mementos. Dependent on Memgator API'''
	memento_list = m.getMementos(uri)
	assert len(memento_list) >= expectedCount
	for i in memento_list:
		for key, value in i.items():
			# for each dictionary key there should be some value.
			assert value


@pytest.mark.parametrize("uri, memDate", [
	("http://web.archive.org/web/19970102130137/http://cs.odu.edu:80/", "1996-02-09T21:47:46"),
	("http://arquivo.pt/wayback/20091223043049/http://www.cs.odu.edu/", "2009-12-23T04:30:50"),
])
def test_getRealDate(uri, memDate):
	realDate = m.getRealDate(uri, memDate)
	assert realDate == memDate


@pytest.mark.skip(reason='not implemented')
def testGetArchives(uri, earliestDate):
	'''
	Calls getMementos and getRealDate to form a json dictionary.
	'''
	pass
