from __future__ import unicode_literals

import json

from django.db import models


class KeyValueSettingManager(models.Manager):
    def get_value(self, key):
        """
        Gets a setting's value by the key.

        Inputs:

            key = The key of the setting

        Returns:

            value (str) = The setting's value
        """
        key_value_setting = super(KeyValueSettingManager, self).get_queryset().get(key=key)
        return key_value_setting.value

    def get_dict_value(self, key):
        """
        Gets a setting's value by the key. The value is returned as a dict. If the
        value is not a valid JSON string, ValueError is raised.

        Inputs:

            key = The key of the setting

        Returns:

            value (dict) = The setting's value
        """
        key_value_setting = super(KeyValueSettingManager, self).get_queryset().get(key=key)
        return json.loads(key_value_setting.value)

    def get_dict_value_or_none(self, key):
        """
        Gets a setting's value by the key. If the value is not a valid JSON string,
        None is returned, else a dict is returned.

        Inputs:

            key = The key of the setting

        Returns:

            value (None or dict) = The setting's value
        """
        key_value_setting = super(KeyValueSettingManager, self).get_queryset().get(key=key)
        try:
            return json.loads(key_value_setting.value)
        except ValueError:
            return None

    def get_or_create_value(self, key):
        """
        Gets a setting's value by the key. If the setting with the key doesn't exist,
        a setting is created with value as an empty string and then the value is
        returned as a string.

        Inputs:

            key = The key of the setting

        Returns:

            value (str) = The setting's value
            created (bool) = If the setting was created, True is returned, else False
        """
        created = False
        try:
            key_value_setting = super(KeyValueSettingManager, self).get_queryset().get(key=key)
        except KeyValueSetting.DoesNotExist:
            key_value_setting = KeyValueSetting(key=key, value='')
            created = True
            key_value_setting.save()
        return key_value_setting.value, created

    def get_or_create_dict_value(self, key):
        """
        Gets a setting's value by the key. If the setting with the keydoesn't exist,
        a setting is created with value as an empty string and then the value is
        returned as a dict.

        Inputs:

            key = The key of the setting

        Returns:

            value (dict) = The setting's value
            created (bool) = If the setting was created, True is returned, else False
        """
        created = False
        try:
            key_value_setting = super(KeyValueSettingManager, self).get_queryset().get(key=key)
        except KeyValueSetting.DoesNotExist:
            key_value_setting = KeyValueSetting(key=key, value='{}')
            created = True
            key_value_setting.save()
        return json.loads(key_value_setting.value), created


class KeyValueSetting(models.Model):
    key = models.CharField(
        unique=True,
        max_length=255)
    value = models.TextField()
    notes = models.TextField(
        blank=True)
    added_on = models.DateTimeField(
        auto_now_add=True)
    updated_on = models.DateTimeField(
        auto_now=True)

    objects = KeyValueSettingManager()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'key value setting'
        verbose_name_plural = 'key value settings'
