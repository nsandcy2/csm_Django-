"""
URL configuration for project_csm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include("core.urls")),   # core routes
    path("crms/", include("crms.urls")), # crms routes
    path("fsrm/", include("fsrm.urls")),  # fsrm routes
    path("safety_plan/", include("safety_plan.urls")),  # safety_plan routes
    path("wp1/", include("wp1.urls")),  # wp1 routes
    path("wp2/", include("wp2.urls")),  # wp2 routes
    path("wp3/", include("wp3.urls")),  # wp3 routes
    path("wp4/", include("wp4.urls")),  # wp4 routes
    path("wp5/", include("wp5.urls")),  # wp5 routes
   
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

