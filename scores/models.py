import json
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
import statistics


class Classmate(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    classnumber = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    classdate = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True)
    unit_id = models.IntegerField(null=True)
    unit_name = models.CharField(max_length=64, null=True)
    training_id = models.IntegerField(null=True)
    CLASS_STATUS = (
        ('0', '中離'),
        ('1', '成功'),
        ('2', '失敗')
    )

    status = models.CharField(
        max_length=10,
        choices=CLASS_STATUS,
        blank=True,
        default='open',
    )

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        new_avg = Course.objects.get(coursenumber=str(self.classnumber).split("-")[0])
        new_avg.save()


    def delete(self, *args, **kwargs):
        # 在刪除前執行必要的任務
        new_avg = Course.objects.get(coursenumber=str(self.classnumber).split("-")[0])
        super().delete(*args, **kwargs)
        new_avg.save()

    def __str__(self):
        return self.name.username


class Course(models.Model):
    coursenumber = models.AutoField(primary_key=True)
    coursename = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('End date must be after start date.')

    coursepeople = models.CharField(max_length=100, null=True)
    Avg_score = models.FloatField(default=0, null=True)
    Median_score = models.FloatField(default=0, null=True)
    course_image = models.ImageField(upload_to='images/', null=True, blank=True)
    introduce = models.TextField(max_length=100, help_text='Enter course introduce', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 调用父类的 save 方法以便保存实例
        try:
            # 计算该课程的平均分数
            average_score = round(
                Classmate.objects.filter(classnumber=self).aggregate(avg_score=Avg('score'))['avg_score'], 1)
            # 获取分数列表
            scores = Classmate.objects.filter(classnumber=self).values_list('score', flat=True)
            self.coursepeople = len(scores)
            scores_list = list(scores)
            if average_score is not None:
                self.Avg_score = average_score
                self.Median_score = statistics.median(scores_list)
            else:
                self.Avg_score = 0  # 如果没有学生的成绩，则平均分数为 0
                self.Median_score = 0
            # 重新保存课程实例，以便更新平均分数
            super().save(*args, **kwargs)
        except Exception as e:
            print(e)

    def __str__(self):
        return f"{self.coursenumber} - {self.coursename}"


class TrainingResult(models.Model):
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=64)
    unit_id = models.IntegerField()
    unit_name = models.CharField(max_length=64)
    start_date = models.DateTimeField()
    training_time = models.IntegerField()
    events = models.TextField()
    score = models.IntegerField()
    result = models.IntegerField()

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # 调用父类的 save 方法以便保存实例
        data = json.loads(str(self.events))
        # print(str(self.events))

        for eve in data:
            model = EventResult(training_id=self, user_id=self.user_id, course_id=self.course_id, unit_id=self.unit_id,
                                start_date=self.start_date, event_id=eve["event_id"], event_name=eve["event_name"],
                                time=eve["time"], score=eve["score"], comment=eve["comment"])
            model.save()
        if len(Course.objects.filter(coursenumber=self.course_id)) == 0:
            model2 = Course(coursenumber=self.course_id, coursename=str(self.course_name)+"-"+str(self.unit_name), start_date=self.start_date)
            model2.save()
        classuser = User.objects.get(pk=self.user_id)
        trainCourse = Course.objects.get(coursenumber=self.course_id)
        if self.score == 0:
            self.result = 0  # 中離
        elif self.score >= 60:
            self.result = 1  # 成功
        else:
            self.result = 2  # 失敗
        model3 = Classmate(name=classuser,classnumber=trainCourse, classdate=self.start_date, score=self.score,
                            unit_id=self.unit_id, unit_name=self.unit_name, training_id=self.pk, status=str(self.result))
        model3.save()


    def __str__(self):
        return f"{self.user_id} - {self.pk}"


class EventResult(models.Model):
    training_id = models.ForeignKey(TrainingResult, on_delete=models.CASCADE, null=True)
    user_id = models.IntegerField( null=True)
    course_id = models.IntegerField( null=True)
    unit_id = models.IntegerField( null=True)
    start_date = models.DateTimeField( null=True)
    event_id = models.IntegerField( null=True)
    event_name = models.CharField(max_length=64)
    time = models.IntegerField( null=True)
    score = models.IntegerField( null=True)
    comment = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.pk} - {self.event_name}"
