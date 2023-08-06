"""Send events to SQS for processing by notification-centre.
"""
import logging

import six

from boto.exception import SQSError, SQSDecodeError, BotoServerError

from django.conf import settings

from rest_framework import serializers

from .exceptions import NotificationClientException
from .serializers import EventSerializer


logger = logging.getLogger(__name__)  # pylint: disable=C0103


def _validate_event_name(event_name):
    """Reject empty event_name.
    """
    if not event_name:
        raise NotificationClientException(
            "Notification events must have a non-empty event_name argument.")

    return event_name


def _validate_links(links, link):
    """Return link if it's specified and links isn't; an empty string if
    neither is specified; otherwise return links.
    """
    if not links:
        if link:
            links = link
        else:
            links = ''

    return links


def _get_user(request):
    """Pull out and return the user's ID and email from a given request,
    or (None, '') if the request is None.
    """
    if request:
        user_id = request.user.id
        user_email = request.user.email
    else:
        user_id = None
        user_email = ''

    return user_id, user_email


def _send_event(event_name, organisation_id, request=None, user_outgoing=None,
                email_outgoing='', links=None, link=None, extra=None,
                related_obj=None):
    """Send an event to the notifications-centre server.

    @param event_name: the type of event
    @param organisation_id: the active organisation's ID
    @param request: the request that triggered this event (the user's details
        are retrieved from this - may be left unspecified for 'all user'
        notifications)
    @param user_outgoing: the user to deliver the notification to (same as
        the triggering user if unspecified)
    @param email_outgoing: the email address of the user to whom the
        notification will be delivered (same as that of the triggering user if
        unspecified)
    @param link: deprecated - will be mapped onto links if links isn't used
    @param links: the location that the user will be taken to after clicking
        the notification. Either a single string, or a dict in the format
        {link_name: url}
    @param extra: additional event information
    @param related_obj: an object ID used to identify this event in the future
    """

    user_id, user_email = _get_user(request)

    data = {
        'event_name': event_name,
        'user_incoming': user_id,
        'email_incoming': user_email,
        'user_outgoing': user_outgoing,
        'email_outgoing': email_outgoing,
        'organisation': organisation_id,
        'links': links if links is not None else link,
        'related_obj': related_obj,
        'extra': extra if extra is not None else {},
    }

    serialized = EventSerializer(data=data)

    try:
        serialized.is_valid(raise_exception=True)
    except serializers.ValidationError:
        raise NotificationClientException(serialized.errors)

    serialized.save()


def send_event(*args, **kwargs):
    """A wrapper for _send_event() so that the user may elect to ignore
    exceptions.
    """

    if getattr(settings, 'NOTIFICATION_CLIENT_IGNORE_EXCEPTIONS', False):
        exceptions_to_ignore = (SQSError, SQSDecodeError, BotoServerError)
    else:
        exceptions_to_ignore = ()

    try:
        _send_event(*args, **kwargs)
    except exceptions_to_ignore as e:
        logger.exception('Ignored exception: %s', six.text_type(e))
