from django.contrib import admin
from .models import ChangeRequest, ImpactAnalysis

@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('change_request_id', 'start_date', 'phase', 'end_date')
    search_fields = ('change_request_id',)
    list_filter = ('phase', 'phase_status')

@admin.register(ImpactAnalysis)
class ImpactAnalysisAdmin(admin.ModelAdmin):
    list_display = ('change_request', 'start_date', 'due_date', 'change_severity')
    search_fields = ('change_request__change_request_id',)
    list_filter = ('change_severity', 'phase_status')