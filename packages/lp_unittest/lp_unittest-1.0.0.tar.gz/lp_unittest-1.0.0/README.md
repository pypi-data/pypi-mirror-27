# django-rest-unit-tests
> A Python Package for Django + Django Rest Framework

## Usage
| **Project** | **Version**|
| :--------:  | ---------- |


## Installation
```bash
pip install lp_unittest
```

## Usage
```python
from lp_unittest.base import BaseRestUnitTest


class YourTestCase(BaseRestUnitTest):
    fixtures = ['someFixturesYouNeed',]
    url = 'yourview_name'
```



## Development Documentation
### Setup Development Environment
```
# Setup a virtual environment
virtualenv -p $(which python3) env

# Activate virtual environment
source env/bin/activate

# Setup Django
pip install -r requirements.txt
ln -s ../lp_accounts testproject
python manage.py migrate

# Run Server
python manage.py runserver
```

### Admin Access
[Admin URL](http://127.0.0.1:8000/admin)
  - Username: `hello@launchpeer.com`
  - Password: `97irwAQza4A/YfFwHNvOUWWataHrC9R8imxxnOz1fwQ=`

### Testing
```
python manage.py test testproject
```

## Publishing to PyPi
### `.pypirc`
Install this file to `~/.pypirc`
```python
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: launchpeer
password: DoD5T5bNzC5+JQZczvwYO+pBNGqp+zg2idVzEtH2gUs=

[testpypi]
repository: https://test.pypi.org/legacy/
username: launchpeer
password: DoD5T5bNzC5+JQZczvwYO+pBNGqp+zg2idVzEtH2gUs=
```

### Deploy to PyPiTest
```
python setup.py sdist upload -r testpypi
```

### Deploy to PyPi
```
python setup.py sdist upload -r pypi
```
