from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoUserModel
from django.utils.translation import gettext_lazy as _

from articles.models import Article

class User(DjangoUserModel):
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user can alter in this admin site."),
    )
    favorites = models.ManyToManyField(
        Article,
        verbose_name=_("favorites list"),
        help_text=_("Designates the list of articles liked by users."),
    )

    REQUIRED_FIELDS = [*DjangoUserModel.REQUIRED_FIELDS, 'first_name', 'last_name']

    class Meta:
        ordering = ["date_joined"]