"""Models module."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from cerberus_ac.models import RoleMixin


class User(AbstractUser, RoleMixin):
    """Simple User model derived from Django's abstract user."""

    email_confirmed = models.BooleanField(default=False)
