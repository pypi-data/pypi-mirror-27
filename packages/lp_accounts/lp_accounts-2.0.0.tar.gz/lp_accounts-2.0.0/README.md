# django-rest-account
> A Python Package for Django + Django Rest Framework

## Glossary  
  - [Usage](#usage)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [How To's](#how-tos)
  - [Development Documentation](#development-documentation)
  - [Publishing a Release](#publishing-to-pypi)

## Usage
| **Project** | **Version**|
| :--------:  | ---------- |
|[Quadco](https://github.com/Launchpeer/quadco-backend)|[v0.1.9](https://github.com/Launchpeer/django-rest-account/releases/tag/v0.1.9)|
|[The Modern Testament](https://github.com/Launchpeer/the-modern-testament-backend)|[v0.1.9](https://github.com/Launchpeer/django-rest-account/releases/tag/v0.1.9)|
|[Gotcha](https://github.com/Launchpeer/gotcha-backend)|[v0.1.9](https://github.com/Launchpeer/django-rest-account/releases/tag/v0.1.9)|
|[Launchbids](https://github.com/Launchpeer/launchbids-backend)|[v1.2.0](https://github.com/Launchpeer/django-rest-account/releases/tag/v1.2.0)|

## Installation
```bash
pip install lp_accounts
```

Add the following to the bottom of `urls.py`
```python
urlpatterns += [url(r'^', include('lp_accounts.urls'))]
```

## Configuration
### Configure _Welcome Email_
The following configuration is provided by default
```python
TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

LP_ACCOUNTS_WELCOME_EMAIL_ENABLED = False
LP_ACCOUNTS_WELCOME_EMAIL_TEMPLATE = 'welcome'
LP_ACCOUNTS_WELCOME_EMAIL_SENDER = 'support@launchpeer.com'
LP_ACCOUNTS_WELCOME_EMAIL_SUBJECT = 'Welcome to our site!'
```
### Configure _Reset Password Email_
The following configuration is provided by default
```python
LP_ACCOUNTS_PASSWORD_RESET_TEMPLATE = 'passwordreset'
LP_ACCOUNTS_PASSWORD_RESET_SENDER = 'support@launchpeer.com'
```

### Configure _Social Authentication_
See [Python Social Auth Docs](http://python-social-auth.readthedocs.io/en/latest/backends/index.html#social-backends)

## How To's
### How to Extend User Model to Provide Custom Fields
`./testproject/employee/models.py`
```
from django.db import models
from lp_accounts.models import BaseAccount


class Employee(BaseAccount):
    bio = models.CharField(max_length=255)


class Manager(BaseAccount):
    department = models.CharField(max_length=255)
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
  - Password: `l6Jw7Dhrsb8WqGca8gBFmivWh7/kHSLNfARvjqWKnKw=`


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
