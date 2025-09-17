from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),   #  home route
    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),

    # Projects
    path("add_project/", views.add_project, name="add_project"),
    path("assign_project/", views.assign_project, name="assign_project"),
    path("work_products/<int:project_id>/", views.work_products, name="work_products"),


    # File upload page
    path("index/", views.index, name="index"),

    # Excel handling
    path("upload/", views.upload, name="upload"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("download/", views.download, name="download"),
]
