"""genre_classification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from genre_classification.views import handle_file_upload,handle_prediction_data
from admins.views import admin_view, activate_model

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='genre_classification/home.html'), name='login'),
    path('admin/', admin_view, name='admin'),
    path('activate_model/', activate_model, name='activate_model'),
    path('', handle_file_upload, name='home'),
    path('django/admin', admin.site.urls),
    path('predictions/', auth_views.LoginView.as_view(template_name='genre_classification/predictions.html'), name='predictions'),
    path('predictions/data',handle_prediction_data,name='handle_prediction_data')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
