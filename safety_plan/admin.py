from django.contrib import admin
from .models import SafetyPlanDetail

@admin.register(SafetyPlanDetail)
class SafetyPlanDetailAdmin(admin.ModelAdmin):
    list_display = ("project_workproduct", "summary")
    search_fields = ("project_workproduct__project__name", "project_workproduct__workproduct__name")
