# paperswithcode.com API client

This is a client for [PapersWithCode](https://paperswithcode.com/api/v1/docs/)
read/write API.

The API is completely covered by the client and it wraps all the API models
into python objects and communicates with the API by getting and passing those
objects from and to the api client.

Documentation can be found on the
[ReadTheDocs](https://paperswithcode-client.readthedocs.io/en/latest/) website.

It is published to the
[Python Package Index](https://pypi.org/project/paperswithcode-client/) and
can be installed by simply calling `pip install paperswithcode-client`.

## Quick usage example

```python

from paperswithcode import PapersWithCodeClient

client = PapersWithCodeClient()
papers = client.paper_list()
print(papers.results[0])
print(papers.next_page)
```
