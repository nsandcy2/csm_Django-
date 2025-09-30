from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import SafetyPlanDetail

@admin.register(SafetyPlanDetail)
class SafetyPlanDetailAdmin(SimpleHistoryAdmin):
    list_display = ("project_workproduct", "owner", "summary")
    search_fields = ("project_workproduct__project__name", "owner")