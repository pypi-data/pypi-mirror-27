# Django Key Value Settings
A small app for storing meta information for a Django app as KV pairs.
The settings are stored in the database.

## Version

0.1.0

## Features

* Stores meta-information/settings required by a typical project, for e.g the "License"
* The value can be fetched directly as dict or in it's raw form

## Dependencies

* Django 1.7 or above

## Installation

* Using pip

```
pip install django_rest_swagger_enhancer
```

## Setup

* Add the following in your settings.py file

```
INSTALLED_APPS = [
    ...
    'kv_settings',
    ...
]
```
