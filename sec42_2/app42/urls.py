from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('upload', views.upload, name = 'upload'),
    path('download/<id>', views.download, name = 'download'),
    path('download_go/<id>', views.download_go, name = 'download_go'),
]