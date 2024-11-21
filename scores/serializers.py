from rest_framework import serializers
from .models import TrainingResult,EventResult
from django.contrib.auth.models import User
class TrainingResultSerializer(serializers.ModelSerializer):
  class Meta:
    model = TrainingResult
    fields = ['user_id',
              'course_id',
              'course_name',
              'unit_id',
              'unit_name',
              'start_date',
              'training_time',
              'events',
              'score',
              'result']


class EventResultSerializer(serializers.ModelSerializer):
  class Meta:
    model = EventResult
    fields = ['training_id',
              'event_id',
              'event_name',
              'time',
              'score',
              'comment']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password']