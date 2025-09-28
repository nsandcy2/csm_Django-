from django.db import models
from core.models import ProjectWorkProduct

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

    def __str__(self):
        return f"Safety Plan for {self.project_workproduct.project.name}"
