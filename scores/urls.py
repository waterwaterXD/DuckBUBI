from django.urls import path, re_path
from . import views


app_name = 'scores'

urlpatterns = [
    path('student-grades/', views.student_scorefind, name="student-grades"),
    path('add/', views.add, name='add'),
    path('course-list/', views.detail, name='detail'),
    path('delete/<pk>/', views.delete_course, name='delete'),
    path('score_find/', views.admin_coursefind, name='score_find'),
    path('score_find/<course_number>', views.admin_scorefind, name='admin_score_find'),
    path('score_find/<course_number>/<train_pk>', views.training_result_user, name='admin_score_find'),
    path('analysis_chart/', views.analysis_chart, name='analysis_chart'),
    path('event_result/', views.event_result, name='event_result'),
    path('training_result/', views.training_result, name='training_result'),
    path('honors/', views.honors, name='honors'),
    re_path(r'^bar/$', views.ChartView.as_view()),
    re_path(r'^event_bar/$', views.Event_ChartView.as_view()),
    re_path(r'^train_bar/$', views.Training_ChartView.as_view(), name='train_bar'),


]