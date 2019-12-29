# pydrugshortagesca

A minimal python wrapper around the [drugshortagescanada.ca](https://drugshortagescanada.ca) database API

Depends on `requests` module and will pass through exceptions from that library when they occur. 

## Installation

Uses [poetry](https://python-poetry.org/) (e.g. `pip install poetry` first). 

```
poetry install
```


## Usage


## Testing

Create a file `.api` that contains your username and password for `canadadrugshortages.ca` on one line, e.g. 

```
me@azurediamond.com hunter2
```

Then run `poetry run pytest`
