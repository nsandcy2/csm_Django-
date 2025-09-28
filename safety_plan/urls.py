from django.urls import path
from . import views

urlpatterns = [
    path("tailor/<int:project_id>/", views.tailor_safety_plan, name="tailor_safety_plan"),
]
