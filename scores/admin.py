from django.contrib import admin

# Register your models here.
from .models import Classmate,Course,TrainingResult,EventResult
class ClassmatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'classnumber', 'classdate', 'score','status')

admin.site.register(Classmate, ClassmatesAdmin)


class CoursesAdmin(admin.ModelAdmin):
    list_display = ('coursenumber', 'coursename', 'start_date','end_date', 'coursepeople','Avg_score','Median_score')
admin.site.register(Course, CoursesAdmin)

class TrainingResultAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'course_id', 'course_name','unit_id', 'unit_name','start_date','training_time','events','score','result')
admin.site.register(TrainingResult, TrainingResultAdmin)


class EventResultAdmin(admin.ModelAdmin):
    list_display = ('training_id', 'event_id', 'event_name','time', 'score','comment')
admin.site.register(EventResult, EventResultAdmin)
