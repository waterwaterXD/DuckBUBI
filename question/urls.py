#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path,re_path

from . import views

app_name = 'question'

urlpatterns = [
    path('question_list/', views.question_list, name='question_list'),
    path('questionnaire/<int:questionnaire_id>/', views.get_questionnaire, name='get_questionnaire'),
    path('vote/', views.submit_vote, name='vote'),
    path('question_analyis/',views.analysis_chart,name='question_analyis'),
    re_path(r'^que_bar/$', views.Que_ChartView.as_view()),
]
