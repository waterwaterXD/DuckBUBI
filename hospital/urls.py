from django.urls import path, re_path
from . import views


app_name = 'hopital'

urlpatterns = [
    path('', views.index2, name="index2"),

]