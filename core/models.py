from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Custom User with role support
class User(AbstractUser):
    role = models.CharField(max_length=20, default="user")  # admin or user

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    users = models.ManyToManyField(User, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkProduct(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    app_label = models.CharField(max_length=50, blank=True)  # e.g., 'safetyplan', 'wp_risk'
    is_safety_plan = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProjectWorkProduct(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_workproducts")
    workproduct = models.ForeignKey(WorkProduct, on_delete=models.CASCADE)
    tailored_out = models.BooleanField(default=False)
    tailored_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tailored_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("project", "workproduct")

    def save(self, *args, **kwargs):
        if self.tailored_out and not self.tailored_at:
            self.tailored_at = timezone.now()
        super().save(*args, **kwargs)
        # Log every save
        ProjectWorkProductLog.objects.create(
            project=self.project,
            workproduct=self.workproduct,
            tailored_out=self.tailored_out,
            tailored_by=self.tailored_by,
        )

    def __str__(self):
        status = "Tailored Out" if self.tailored_out else "Included"
        return f"{self.project.name} - {self.workproduct.name} ({status})"


class ProjectWorkProductLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    workproduct = models.ForeignKey(WorkProduct, on_delete=models.CASCADE)
    tailored_out = models.BooleanField(default=False)
    tailored_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tailored_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Tailored Out" if self.tailored_out else "Included"
        return f"[{self.tailored_at:%Y-%m-%d %H:%M}] {self.project.name} - {self.workproduct.name} {status}"