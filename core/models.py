from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User with role support
class User(AbstractUser):
    role = models.CharField(max_length=20, default="user")  # "admin" or "user"

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_projects")
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.name

class WorkProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="workproducts")
    enabled = models.BooleanField(default=True)  # lets you enable/disable per project

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"
