from django.urls import path
from . import views

urlpatterns = [
    path('', views.index2),
    path('student-information/', views.student_information),
    path('student-revise/', views.student_revise),
    path('chatroom/', views.chatroom),
    path('contact/', views.contact),
    path('aboutus/', views.aboutus),
    path('ebook/', views.ebook),
    path('hospital/', views.hospital),
    path('get_locations/', views.get_locations, name='get_locations'),
    path('search_clinics/', views.search_clinics, name='search_clinics'),
    path('video/', views.video),
    path('questionnaire/', views.questionnaire),
    path('depression/', views.depression),

]