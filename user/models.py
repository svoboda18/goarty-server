from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser as DjangoUserModel
from django.utils.translation import gettext_lazy as _

class User(DjangoUserModel):
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user can alter in this admin site."),
    )

    REQUIRED_FIELDS = [*DjangoUserModel.REQUIRED_FIELDS, 'first_name', 'last_name']

    class Meta:
        ordering = ["date_joined"]