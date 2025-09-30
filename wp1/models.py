from django.db import models
from core.models import ProjectWorkProduct
from simple_history.models import HistoricalRecords

class WP1Detail(models.Model):
    project_workproduct = models.OneToOneField(
        ProjectWorkProduct,
        on_delete=models.CASCADE,
        related_name="wp1_detail"
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="draft")

    history = HistoricalRecords()

    def __str__(self):
        return f"WP1 for {self.project_workproduct.project.name}"
