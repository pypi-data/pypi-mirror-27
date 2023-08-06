"""Serialize the Events into data objects to send to JSON.
"""
import logging
from uuid import uuid4

import six

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import timezone

from rest_framework import serializers

from queue_fetcher.utils import sqs

logger = logging.getLogger(__name__)  # pylint: disable=C0103


class _StringOrDictField(serializers.DictField):
    """Specialized handler for the links field.
    """

    def to_internal_value(self, data):
        """Map the incoming data into a dict.
        """
        if isinstance(data, six.string_types):
            data = {'link': data}
        return data


class _ModelOrIntegerField(serializers.IntegerField):
    """Specialized handler for integer or Model fields.
    """

    def to_internal_value(self, data):
        """Convert a Django Model into a field.
        """
        if isinstance(data, models.Model):
            return data.pk
        return data


class EventSerializer(serializers.Serializer):
    """Serialize an event from data and context.

    Take the output of .data and pass it straight into the send_message.
    """

    event_name = serializers.CharField()
    organisation = _ModelOrIntegerField()

    user_incoming = serializers.IntegerField(allow_null=True)
    email_incoming = serializers.EmailField(allow_blank=True)

    user_outgoing = serializers.IntegerField(allow_null=True)
    email_outgoing = serializers.EmailField(allow_blank=True)
    links = _StringOrDictField(child=serializers.URLField(), required=False)

    related_obj = serializers.IntegerField(allow_null=True)

    extra = serializers.JSONField()

    link = serializers.URLField(allow_blank=True, required=False)  # DEPRECATED

    def validate(self, validated_data):
        """Add the extra UUID and datetime fields.

        We will also add the user_outgoing and email_outgoing fields here.
        """
        validated_data['uuid'] = str(uuid4())
        validated_data['datetime'] = str(timezone.now())
        validated_data['message_type'] = 'event'

        if validated_data['user_outgoing'] is None:
            validated_data['user_outgoing'] = validated_data['user_incoming']
        if validated_data['email_outgoing'] is None:
            validated_data['email_outgoing'] = validated_data['email_incoming']

        return validated_data

    def save(self):
        """Push the serialized information out to the server.
        """

        validated_data = self.validate(self.data)
        queue_name = getattr(settings, 'AWS_EVENT_QUEUE', False)
        default_region = getattr(settings, 'DEFAULT_SQS_REGION', False)

        if not queue_name:
            raise ImproperlyConfigured(
                'AWS_EVENT_QUEUE has not been configured. Make sure that '
                'it\'s configured in your settings file.')

        if default_region:
            queue = sqs.get_queue(queue_name, region_name=default_region)
        else:
            queue = sqs.get_queue(queue_name)

        sqs.send_message(queue, validated_data)
        logger.info('Sent event %s to SQS', validated_data['uuid'])
