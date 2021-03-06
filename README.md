# pydrugshortagesca

A minimal python wrapper around the [drugshortagescanada.ca](https://drugshortagescanada.ca) database API

Depends on `requests` module and will pass through exceptions from that library when they occur. 

## Installation

Install the package: 

```
pip install pydrugshortagesca
```

You can then configure your `drugshortagescanada.ca` username and password in one of the following ways: 

Create configuration file in `~/.config/pydrugshortagesca/config`:

```sh
email="username@domain.com"
password="s3cr3t!"
```

Or, set the following environment variables: 

```sh
export DSC_EMAIL="username@domain.com"
export DSC_PASSWORD="s3cr3t!"
```

You can test your installation by running the command `pydrugshortagesca`. You
should not be prompted for a username or password, and it should return some
results in JSON format. 

## Basic Usage

Interacting with the `drugshortagescanada.ca` database is done via the
`api.Session` object: 

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
    # search() returns a batch of results.
    # Use the `limit` and `offset` parameters to adjust which batch to return.
    json_results = session.search(term="venlafaxine", offset=20)
    print("Total results {}".format(json_results['total']))

    # isearch() returns an iterator over all records returned by a search.
    # This may make several requests to the database if needed.
    results = session.isearch(term="venlafaxine", orderby='updated_date')
    for rec in results:
        print(rec['updated_date'],rec['en_drug_brand_name'],rec['drug_strength'])

    # Custom filter functions can also be supplied
    results = session.isearch(_filter=lambda x: x['drug_strength'] == '150.0MG',
        term="venlafaxine", orderby='updated_date'):
    for rec in results:
        print(rec['updated_date'],rec['en_drug_brand_name'],rec['drug_strength'])
    
    # The export module provides utility functions for exporting results in tabular form
    csvfile = open('shortages.csv','w')
    export.as_csv(session, csvfile, shortages=True, term="venlafaxine")
```

## CLI 

There is also a commandline interface. See `pydrugshortagesca --help` for details, but briefly:

```sh
$ pydrugshortagesca -p term venlafaxine --type shortages --fmt csv > shortages.csv
```

## License

MIT

## Contributing

Pull requests are very welcome!
