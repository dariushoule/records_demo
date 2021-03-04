Records Demo Application
------------------------

_Records Demo_ is a small CLI / HTTP based application that demonstrates:
- File input and transformation
- Basic HTTP/REST concepts

### Setup

Application requires Python >3.9 and [pipenv](https://pipenv.pypa.io/en/latest/)

#### Install Dependencies
```
pipenv install
```

### Usage

#### From the command line
```
pipenv run python records.py
```

#### As a REST API
```
pipenv run python records.py
```

#### Generating sample inputs to test with
```
pipenv run python scripts/generate_sample_inputs.py
```

### Linting

From the project root:
`pipenv run cd .. && pylint records-demo`

### Unit Testing