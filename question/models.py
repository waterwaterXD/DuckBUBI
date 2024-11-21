from typing import Any
from django.db import models

# Create your models here.


class Questionnaire(models.Model):
    title = models.CharField(max_length=200)
    coursename = models.CharField(max_length=200,  default="Coursename")
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return  f'<{self.coursename}:{self.title}>'


# 问题
class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    is_checkbox = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def get_questionnaire_title(self):
        return self.questionnaire.title

    def get_chioce_count(self):
        return self.choice_set.count()

    def get_vote_count(self):
        _count = 0
        for choice in self.choice_set.all():
            _count += choice.votes
        return _count


    get_questionnaire_title.short_description = 'questionnaire'
    get_chioce_count.short_description = 'Total chioce'
    get_vote_count.short_description = 'Total votes'


# 选择
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# 用户
class User(models.Model):
    gender = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    seniority = models.CharField(max_length=200)
    message = models.CharField(max_length=500, null=True)
    message2 = models.CharField(max_length=500, null=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f'<{self.gender}:{self.age}>'


    def __setattr__(self, name, value: Any) -> None:
        super().__setattr__(name, value)


