# Quickstart

Library is designed to work with python objects. All of the models used as
return values in the library are described in the API part of the
documentation.

To use the library you only need to import and instantiate the client and
start calling methods on it:


```python
>>> from paperswithcode import PapersWithCodeClient 
>>> client = PapersWithCodeClient()
>>> papers_page = client.paper_list()
>>> papers_page.count
175834
>>> papers_page.next_page
2
>>> paper = papers_page.results[0]
>>> paper.id
'efficient-methods-for-incorporating-knowledge'
>>> paper.title
'Efficient Methods for Incorporating Knowledge into Topic Models'
```

Same principle is used for all models.

```python
>>> dataset_page = client.dataset_list()
>>> dataset_page.count
2782
>>> dataset_page.results[0].id
'hci'
>>> dataset_page.results[0].name
'HCI'
```

For nested queries you will need to provide the required id's:


```python

>>> conference_page = client.conference_list()
>>> conference = conference_page.results[0]
>>> conference.id
'eccv'
>>> proceedings_page = client.proceeding_list(conference_id=conference.id)
>>> proceeding = proceedings_page.results[0]
>>> proceeding.id
'eccv-2018'
>>> papers = client.proceeding_paper_list(
    conference_id=conference.id, proceeding_id=proceeding.id
)
>>> papers[0].title
'Person Search by Multi-Scale Matching'
``` 