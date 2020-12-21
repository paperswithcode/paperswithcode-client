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

To install:

```bash
pip install paperswithcode-client
```

To list papers indexed on Papers with Code:

```python

from paperswithcode import PapersWithCodeClient

client = PapersWithCodeClient()
papers = client.paper_list()
print(papers.results[0])
print(papers.next_page)
```

For full docs please see our [ReadTheDocs](https://paperswithcode-client.readthedocs.io/en/latest/) page.

## How to mirror your competition

Papers with Code offers a mirroring service for ongoing competitions that allows competition administrators
to automatically upload the results to Papers with Code using an API. 

To use the API in the write mode you'll need to first [obtain an API token](https://paperswithcode.com/accounts/generate_api_token).

Using the API token you'll be able to use the client in write mode:

```python
from paperswithcode import PapersWithCodeClient

client = PapersWithCodeClient(token="your_secret_api_token")
```

To mirror a live competition, you'll need to make sure the corresponding task (e.g. "Image Classification") 
exists on Papers with Code. You can use the search to check if it exists, and if it doesn't, you can add a 
new task on the [Task addition page](https://paperswithcode.com/add/task). 

If you cannot find your dataset on the website, you can create it with the API like this:

```python
from paperswithcode.models.dataset import *
client.dataset_add(
    DatasetCreateRequest(
        name="VeryTinyImageNet",
    )
)
```

Now we are ready to programatically create the competition on Papers with Code. Here is an example of how we would do
this on a fictional VeryTinyImageNet dataset.

```python
from paperswithcode import PapersWithCodeClient
from paperswithcode.models.evaluation.synchronize import *

client = PapersWithCodeClient(token="your_secret_api_token")

r = EvaluationTableSyncRequest(
    task="Image Classification",
    dataset="VeryTinyImageNet",
    description="Optional description of your challenge in markdown format",
    metrics=[
        MetricSyncRequest(
            name="Top 1 Accuracy",
            is_loss=False,
        ),
        MetricSyncRequest(
            name="Top 5 Accuracy",
            is_loss=False,
        )
    ],
    results=[
        ResultSyncRequest(
            metrics={
                "Top 1 Accuracy": "85",
                "Top 5 Accuracy": "95"
            },
            paper="",
            methodology="My Unpublished Model Name",
            external_id="competition-submission-id-4321",
            evaluated_on="2020-11-20",
            external_source_url="https://my.competition.com/leaderboard/entry1"
        ),
        ResultSyncRequest(
            metrics={
                "Top 1 Accuracy": "75",
                "Top 5 Accuracy": "81"
            },
            paper="https://arxiv.org/abs/1512.03385",
            methodology="ResNet-50 (baseline)",
            external_id="competition-submission-id-1123",
            evaluated_on="2020-09-20",
            external_source_url="https://my.competition.com/leaderboard/entry2"
        )
    ]
)

client.evaluation_synchronize(r)
```
This is going to add two entries to the leaderboard, a `ResNet-50` baseline that is referenced by the provided 
arXiv paper link, and an unpublished entry for model `My Unpublished Model Name`. 

To decompose it a bit more:

```python
metrics=[
    MetricSyncRequest(
        name="Top 1 Accuracy",
        is_loss=False,
    ),
    MetricSyncRequest(
        name="Top 5 Accuracy",
        is_loss=False,
    )
],
```

This defines two global metrics that are going to be used in the leaderboard. The table will be ranked based on the 
first provided metric. The paramter `is_loss` indicates if the metric is a loss metric, i.e. if smaller-is-better. 
Since in this case both are accuracy metric where higher-is-better, we set `is_loss=False` which will produce the
correct sorting order in the table. 

An individual row in the leaderboard is represented by:

```python
ResultSyncRequest(
    metrics={
        "Top 1 Accuracy": "85",
        "Top 5 Accuracy": "95"
    },
    paper="",
    methodology="My Unpublished Model Name",
    external_id="competition-submission-id-4321",
    evaluated_on="2020-11-20",
    external_source_url="https://my.competition.com/leaderboard/entry1"
)
```

Metrics is simply a dictionary of metric values for each of the global metrics. The `paper` parameter can be a link
to an arXiv paper, conference paper, or a paper page on Papers with Code. Any code that's associated with the paper
will be linked automatically. The `methodology` parameter should contain
the model name that is informative to the reader. `external_id` is your ID of this submission - this ID should be
unqiue and is used when you make repeated calls to merge results if they changed. `evaluated_on` is the date in `YYYY-MM-DD`
format on which the method was evaluated on - we use this to create progress graphs. Finally, `external_source_url` 
is the URL to your website, ideally linking back to this individual entry. This will be linked in the "Result" column
of the leaderboard and will enable users to navigate back to your website. 

Finally, this line of code:

```python
client.evaluation_synchronize(r)
```

This will execute the request on our API and will return you the ID of your leaderboard on Papers with Code. 
You can then access it by going to `https://paperswithcode.com/sota/<your_leaderboard_id>` or find it using 
the site search.  

To keep your Papers with Code leaderboard in sync, you can simply re-post all the entries in your competition
on regular intervals. If a row already exists, it will be merged and no duplicates will be created. 

For in-depth API docs please refer to our [ReadTheDocs](https://paperswithcode-client.readthedocs.io/en/latest/) page.

By using the API you agree that any competition data you submit will be licenced under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

If you need any help contact us on hello@paperswithcode.com. 










