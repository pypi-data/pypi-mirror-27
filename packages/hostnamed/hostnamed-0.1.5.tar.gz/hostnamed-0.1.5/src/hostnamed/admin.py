from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Host


class HostAdmin(admin.ModelAdmin):
    list_display = ["hostname", "description","update_key",  "ip", "update_time"]
    list_filter = ["update_time"]
    search_fields = ["hostname", "description","update_key",  "ip"]
    readonly_fields = ["ip", "update_time"]
    fieldsets = [
        (_("Basic"), {
            "fields": ["hostname", "description", "update_key"],
        }),
        (_("Update Information"), {
            "fields": ["ip", "update_time"],
        }),
    ]

admin.site.register(Host, HostAdmin)
