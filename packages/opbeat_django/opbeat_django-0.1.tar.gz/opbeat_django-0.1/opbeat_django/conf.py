"""Configuration variables magic."""
import os
# This module should be completely functional without django
try:
    from django.conf import settings
except ImportError:
    settings = object()
else:
    from django.core.exceptions import ImproperlyConfigured
    try:
        # we support both opbeat's standard namespaced settings format
        # and simpler one resembling env variables
        OPBEAT_SETTINGS = getattr(settings, "OPBEAT", {})
        ORGANIZATION_ID = (
            OPBEAT_SETTINGS.get("ORGANIZATION_ID") or
            getattr(settings, "OPBEAT_ORGANIZATION_ID", None)
        )
        APP_ID = (
            OPBEAT_SETTINGS.get("APP_ID") or
            getattr(settings, "OPBEAT_APP_ID", None)
        )
        SECRET_TOKEN = (
            OPBEAT_SETTINGS.get("SECRET_TOKEN") or
            getattr(settings, "OPBEAT_SECRET_TOKEN", None)
        )
    except ImproperlyConfigured:
        ORGANIZATION_ID = APP_ID = SECRET_TOKEN = None

# Env vars override django settings
ORGANIZATION_ID = os.environ.get("OPBEAT_ORGANIZATION_ID") or ORGANIZATION_ID
APP_ID = os.environ.get("OPBEAT_APP_ID") or APP_ID
SECRET_TOKEN = os.environ.get("OPBEAT_SECRET_TOKEN") or SECRET_TOKEN

# Env vars for release tracking (do not have equivalent settings)
REV = os.environ.get("RELEASE_HASH")
BRANCH = os.environ.get("RELEASE_BRANCH")
MACHINE = os.environ.get("RELEASE_MACHINE")
