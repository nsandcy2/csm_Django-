from django.urls import path
from . import views
urlpatterns=[
        path('', views.index, name='wp3_index')
]