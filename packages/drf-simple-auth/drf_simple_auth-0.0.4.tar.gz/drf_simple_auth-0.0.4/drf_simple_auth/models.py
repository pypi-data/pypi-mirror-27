from __future__ import absolute_import, unicode_literals

from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AuthToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE
    )
    device_id = models.CharField(max_length=255)

    key = models.CharField(max_length=255, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.key:
            self.key = uuid4().hex

        super(AuthToken, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )

    class Meta:
        unique_together = ('user', 'device_id')

    def __str__(self):
        return 'Token {}'.format(self.user.username)
