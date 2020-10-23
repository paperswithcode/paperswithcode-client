# Working with evaluation tables


First we'll prepare some data so we can have something to work with:

```python

>>> from paperswithcode import PapersWithCodeClient, models
>>> client = PapersWithCodeClient(token='YOUR TOKEN')

# Task
>>> task = client.task_list().results[0]
>>> task.id
'triple-classification'

# Datasets
>>> datasets = client.dataset_list()
>>> dataset_1 = datasets.results[0]
>>> dataset_2 = datasets.results[1]
>>> dataset_1.id, dataset_2.id
('rewrite', 'leitner-et-al-2020')


# Paper
>>> paper = client.paper_list().results[0]
>>> paper.id
'on-the-minimal-teaching-sets-of-two'


# We can now create and manipulate evaluation tables:


>>> et = client.evaluation_create(
...     models.EvaluationTableCreateRequest(
...         task=task.id,
...         dataset=dataset_1.id
...     )
... )
>>> et.id
'triple-classification-on-rewrite-8'


# Get by id:
>>> client.evaluation_get(et.id)
EvaluationTable(
    id='triple-classification-on-rewrite-8', 
    task='triple-classification',
    dataset='rewrite'
)

# Update
>>> et = client.evaluation_update(et.id, models.EvaluationTableUpdateRequest(
...     dataset=dataset_2.id
... ))
>>> et
EvaluationTable(
    id='triple-classification-on-rewrite-8',
    task='triple-classification',
    dataset='leitner-et-al-2020'
)


# Get Metrics
>>> client.evaluation_metric_list(et.id)
[]

# Add a metric
>>> m = client.evaluation_metric_add(
...     et.id,
...     models.MetricCreateRequest(
...         name="some metric",
...         description="Metric description",
...         is_loss=True
...     )
... )
>>> m
Metric(
    id='748dccd5-0a28-432c-98ec-7ab74a127ede',
    name='some metric',
    description='Metric description',
    is_loss=True
)

# Update a metric
>>> m = client.evaluation_metric_update(
...     et.id,
...     m.id,
...     models.MetricUpdateRequest(is_loss=False)
... )
>>> m
Metric(
    id='748dccd5-0a28-432c-98ec-7ab74a127ede',
    name='some metric',
    description='Metric description',
    is_loss=False
)


# Get results
>>> client.evaluation_result_list(et.id)
[]

# Add a result
>>> r = client.evaluation_result_add(
...     et.id,
...     models.ResultCreateRequest(
...         metrics={"some metric": '44'},
...         methodology="Some methodologoy",
...         uses_additional_data=False,
...         paper=paper.id                   # Optional
...     )
... )
>>> r
Result(
    id='81cdfce5-d976-4d29-93a7-23a29118b037',
    best_rank=None,
    metrics={'some metric': '44'},
    methodology='Some methodologoy',
    uses_additional_data=False,
    paper='on-the-minimal-teaching-sets-of-two',
    best_metric=None
)
    
# Update result
>>> r = client.evaluation_result_update(
...     et.id,
...     r.id,   
...     models.ResultUpdateRequest(
...         methodology="Some other methodologoy",
...         uses_additional_data=True,
...     )
... )
>>> r
Result(
    id='81cdfce5-d976-4d29-93a7-23a29118b037',
    best_rank=None,
    metrics={'some metric': '44'},
    methodology='Some other methodologoy',
    uses_additional_data=True,
    paper='on-the-minimal-teaching-sets-of-two',
    best_metric=None
)

# List the results again
>>> client.evaluation_result_list(et.id)
[
    Result(
        id='81cdfce5-d976-4d29-93a7-23a29118b037',
        best_rank=None,
        metrics={'some metric': '44'},
        methodology='Some other methodologoy',
        uses_additional_data=True,
        paper='on-the-minimal-teaching-sets-of-two',
        best_metric=None
    )
]

# Delete a result
>>> client.evaluation_result_delete(et.id, r.id)
>>> client.evaluation_result_list(et.id)
[]
```