from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Project, WorkProduct, ProjectWorkProduct, ProjectWorkProductLog

# Custom User admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    filter_horizontal = ("users",)
    search_fields = ("name", "created_by__username")


@admin.register(WorkProduct)
class WorkProductAdmin(admin.ModelAdmin):
    list_display = ("name", "is_safety_plan", "app_label")
    list_filter = ("is_safety_plan", "app_label")
    search_fields = ("name",)


@admin.register(ProjectWorkProduct)
class ProjectWorkProductAdmin(admin.ModelAdmin):
    list_display = ("project", "workproduct", "tailored_out", "tailored_by", "tailored_at")
    list_filter = ("tailored_out",)
    search_fields = ("project__name", "workproduct__name", "tailored_by__username")


@admin.register(ProjectWorkProductLog)
class ProjectWorkProductLogAdmin(admin.ModelAdmin):
    list_display = ("project", "workproduct", "tailored_out", "tailored_by", "tailored_at")
    list_filter = ("tailored_out",)
    search_fields = ("project__name", "workproduct__name", "tailored_by__username")
