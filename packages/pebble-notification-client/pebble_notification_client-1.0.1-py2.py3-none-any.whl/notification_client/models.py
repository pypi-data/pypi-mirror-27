"""Notification models for the client.

These shouldn't really be used outside the notification-client package itself.
"""


class Event(object):
    """A notification that will be passed into the serializer.

    The output will be sent to the notification server.
    """

    def __init__(self, event_name, organisation, request=None,
                 user_outgoing=None, email_outgoing='', links=None, link=None,
                 extra=None, related_obj=None):
        self.event_name = event_name

        if isinstance(organisation, int):
            self.organisation = organisation
        else:
            self.organisation = organisation.pk

        self.request = request
        self.user_outgoing = user_outgoing
        self.email_outgoing = email_outgoing
        self.links = links if links is not None else link
        self.extra = extra
        self.related_obj = related_obj
