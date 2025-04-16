from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_content, name='upload_content'),
]
