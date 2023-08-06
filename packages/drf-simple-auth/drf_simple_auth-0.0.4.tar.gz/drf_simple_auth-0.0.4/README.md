# drf-simple-auth

[![Build Status](https://travis-ci.org/nickromano/drf-simple-auth.svg?branch=master)](https://travis-ci.org/nickromano/drf-simple-auth)
[![Coverage Status](https://coveralls.io/repos/github/nickromano/drf-simple-auth/badge.svg?branch=master)](https://coveralls.io/github/nickromano/drf-simple-auth?branch=master)
[![PyPi](https://img.shields.io/pypi/v/drf_simple_auth.svg)](https://pypi.python.org/pypi/drf-simple-auth)
![PyPI](https://img.shields.io/pypi/pyversions/drf_simple_auth.svg)
![PyPI](https://img.shields.io/pypi/l/drf_simple_auth.svg)

`drf_simple_auth` extends the `TokenAuthentication` in Django Rest Framework to accomodate separate tokens per device.  This package also has signup and login endpoints for a client to request or create a new token.

## Installation

1) Install the package

```bash
pip install drf_simple_auth
```

2) Add `'drf_simple_auth'` to `INSTALLED_APPS`

3) Add the following to your `urlpatterns`

```python
    url(r'^api/1/auth/', include('drf_simple_auth.urls')),
```

4) Add `drf_simple_auth.auth.SimpleAuthTokenAuthentication` to `DEFAULT_AUTHENTICATION_CLASSES`

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drf_simple_auth.auth.SimpleAuthTokenAuthentication',
    ),
}
```

## Usage

`device_id` is optional and should be generated on the client.

#### Signup

```bash
curl -X "POST" "http://localhost:8000/api/1/auth/signup/" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "username": "test@test.com",
  "password": "testpassword",
  "device_id": "36989fd3-1bcf-4c35-85ed-63089c21a552"
}'
```

#### Login

```bash
curl -X "POST" "http://localhost:8000/api/1/auth/login/" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "username": "test@test.com",
  "password": "testpassword",
  "device_id": "36989fd3-1bcf-4c35-85ed-63089c21a552"
}'
```

#### Authenticated Endpoint

```bash
curl "http://localhost:8000/api/1/myview/" \
     -H "Authorization: DToken d3c93d0ed5634f6fbe2d71c2aefe67bb"
```

## Additional Options

Add `CHECK_USERNAME_IS_EMAIL = True` to `settings.py` to have the signup api validate a username looks like an email address.
