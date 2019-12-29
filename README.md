# pydrugshortagesca

A minimal python wrapper around the [drugshortagescanada.ca](https://drugshortagescanada.ca) database API

Depends on `requests` module and will pass through exceptions from that library when they occur. 

## Installation

Uses [poetry](https://python-poetry.org/). Run `poetry install`. 

## Basic Usage

Interacting with the `drugshortagescanada.ca` database is done via the `api.Session` object: 

```python
from pydrugshortagesca import api, export
import json

session = api.Session(email="name@domain.com", password="123456")

try:
	session.login()
except Exception as e:
	print("Error with log in", e)
	print("Details:", session.response.content)
else: 
	# search() returns a batch of results that can be paged through using
	# the offset parameter
	json_results = session.search(term="venlafaxine", offset=20)
	print("Total results {}".format(json_results['total']))

	# use isearch() to iterate through all of the records (this will send
	# multiple requests to the database)
	results = session.isearch(term="venlafaxine", orderby='updated_date')
	for rec in results:
		print(rec['updated_date'],rec['en_drug_brand_name'],rec['drug_strength'])

	# custom filter functions can also be supplied
	results = session.isearch(_filter=lambda x: x['drug_strength'] == '150.0MG',
		term="venlafaxine", orderby='updated_date'):
	for rec in results:
		print(rec['updated_date'],rec['en_drug_brand_name'],rec['drug_strength'])
	
	# the export module provides utility functions for exporting results in tabular form
	csvfile = open('shortages.csv','w')
	export.as_csv(session, csvfile, shortages=True, term="venlafaxine")
```

## CLI 

There is also an easy to use commandline interface. See `pydrugshortagesca --help` for details, but briefly:

```sh
$ pydrugshortagesca -p term venlafaxine --type shortages --fmt csv > shortages.csv
```

## Testing

Create a file `.api` that contains your username and password for `canadadrugshortages.ca` on one line, e.g. 

```
me@azurediamond.com hunter2
```

Then run `poetry run pytest`
