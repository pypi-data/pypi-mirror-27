from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HostnamedConfig(AppConfig):
    name = 'hostnamed'
    verbose_name = _("Dynamic Hostname Manager")