from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import WP1Detail

@admin.register(WP1Detail)
class WP1DetailAdmin(SimpleHistoryAdmin):
    list_display = ("project_workproduct", "status")
