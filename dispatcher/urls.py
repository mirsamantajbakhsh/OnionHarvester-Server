from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
    path('response', views.response, name='response'),
    path('result', views.result, name='result'),
    path('download', views.download, name='download'),
]
