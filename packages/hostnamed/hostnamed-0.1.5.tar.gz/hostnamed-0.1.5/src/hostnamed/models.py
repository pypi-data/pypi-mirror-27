import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Host(models.Model):
    hostname = models.CharField(max_length=32, unique=True, verbose_name=_("Hostname"))
    description = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("Description"))
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP Address"))
    update_key = models.CharField(max_length=36, verbose_name=_("Update Key"), blank=True)
    update_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Update Time"))

    class Meta:
        verbose_name = _("Host")
        verbose_name_plural = _("Hosts")

    def __str__(self):
        return self.hostname

    def save(self, *args, **kwargs):
        self.hostname = self.hostname.upper()
        if not self.update_key:
            self.update_key = str(uuid.uuid4())
        super(Host, self).save(*args, **kwargs)
