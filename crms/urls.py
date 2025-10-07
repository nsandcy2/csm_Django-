from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='crms_index'),
    path('index/', views.index, name='index'),
    path('new-request/', views.new_request, name='new_request'),
    path('new-request-step2/<str:change_request_id>/', views.new_request_step2, name='new_request_step2'),
    path('existing-change-request/', views.existing_change_request, name='existing_change_request'),


    
    path('existing-change-request/<str:change_request_id>/', views.existing_change_request_step1, name='existing_change_request_step1'),
    path('existing-change-request-step2/<str:change_request_id>/', views.existing_change_request_step2, name='existing_change_request_step2'),
    path('download-db-file/<str:cr_id>/', views.download_db_file, name='download_db_file'),
    path('impact-analysis/', views.impact_analysis, name='impact_analysis'),
    path('checklist/', views.auto_checklist, name='auto_checklist'),
]