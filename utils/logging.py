import logging

from django.conf import settings
from django.utils import timezone


def make_log_message_with_time(message) -> str:
    return timezone.now().strftime("%Y-%m-%d %H:%M:%S") + " " + message


def log_system_event(message):
    if settings.IS_SYSTEM_EVENTS_LOGGING_ENABLED:
        logging.getLogger("system_events").info(make_log_message_with_time(message))


def log_error(message):
    logging.getLogger("").error(make_log_message_with_time(message))
