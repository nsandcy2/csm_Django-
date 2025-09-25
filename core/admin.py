from django.contrib import admin
from .models import User, Project, WorkProduct  # <-- Add WorkProduct here

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'owner', 'created_at')
    list_filter = ('created_at',)

@admin.register(WorkProduct)  # <-- Register WorkProduct
class WorkProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'enabled', 'created_at')
    list_filter = ('project', 'enabled')
    search_fields = ('name', 'description')
