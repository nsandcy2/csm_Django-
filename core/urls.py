from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Authentication paths
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    # Dashboard 
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    # Project management
    path("add_project/", views.add_project, name="add_project"),
    path("work_products/<int:project_id>/", views.work_products, name="work_products"),
    path("assign_project/", views.assign_project, name="assign_project"),
    path("list_of_projects/", views.list_of_projects, name="list_of_projects"),
path("safety_plan/", include("safety_plan.urls")),
    # Excel handling
    path("upload/", views.upload, name="upload"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("download/", views.download, name="download")
]