from django.db import models
from core.models import ProjectWorkProduct
from simple_history.models import HistoricalRecords

class SafetyPlanDetail(models.Model):
    """
    Safety Plan-specific info linked to ProjectWorkProduct
    """
    project_workproduct = models.OneToOneField(
        ProjectWorkProduct,
        on_delete=models.CASCADE,
        related_name="safetyplan_detail"
    )
    summary = models.TextField(blank=True)
    owner = models.CharField(max_length=100, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"Safety Plan for {self.project_workproduct.project.name}"
