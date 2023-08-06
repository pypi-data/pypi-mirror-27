# Django Key Value Settings
A small app for storing meta information for a Django app as KV pairs.
The settings are stored in the database.

## Version

1.0.0

## Features

* Stores meta-information/settings required by a typical project, for e.g the "License" text
* API for storing the data as string or as dict
* The value can be fetched directly as dict or as string

## Dependencies

* Django 1.7 or above

## Installation

* Using pip

```
pip install kv-settings
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

## Properties

* **key:** A unique string to identify the setting.
* **value:** The value of the setting. Can be dict or a str.
* **notes:** A string for comments or notes on the setting.
* **added_on:** Added on datetime.
* **updated_on:** Last updated on datetime.

## Usage

Import it by

```
from kv_settings.models import KeyValueSetting
```

Create a setting

```
setting = KeyValueSetting(key='some_setting', value={'foo': 'bar'})
setting.save()

# Get the value back
setting.value
>>> '{"foo": "bar"}'
setting.value_as_dict
>>> {u'foo': u'bar'}
```

Fetch a setting

```
# Like normal Django model
setting = KeyValueSetting.objects.get_value(key='some_setting')
setting.value
>>> '{"foo": "bar"}'
setting.value_as_dict
>>> {u'foo': u'bar'}

# Get the value only
setting = KeyValueSetting.objects.get_value(key='some_setting')
setting
>>> '{"foo": "bar"}'

# Raises ValueError if the value is not dict serializable
setting = KeyValueSetting.objects.get_dict_value(key='some_setting')
setting
>>> {u'foo': u'bar'}
```

To avoid ValueError being raised, following can be used

```
setting = KeyValueSetting.objects.get_dict_value_or_none(key='some_setting')
>>> {u'foo': u'bar'}  # If a valid dict
>>> None  # If non serializable
```

A new setting can be created if doesn't exist already

```
setting = KeyValueSetting.objects.get_or_create_dict_value(key='some_setting')
setting.value = {'foo': 'bar'}
setting.save()
```
