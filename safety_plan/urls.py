from django.urls import path
from . import views

urlpatterns = [
 path('', views.tailor_safety_plan, name='tailor_safety_plan'),
    path("history/", views.safetyplan_history, name="safetyplan_history")
]
