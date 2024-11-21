from .models import Classmate,Course,EventResult,TrainingResult
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
# Create your views here.

def honors(request):
    # 獲取所有課程
    all_courses = Course.objects.all()

    # 如果用戶選擇了特定的課程，則根據課程過濾學生
    selected_course_number = request.GET.get('course_number')
    if selected_course_number:
        students = Classmate.objects.filter(classnumber__coursenumber=selected_course_number).order_by('-score')[:10]
        selected_course = Course.objects.get(coursenumber=selected_course_number)
        top_students_by_course = [(selected_course, enumerate(students, 1))]  # 包含學生的排名信息
    else:
        # 如果用戶沒有選擇特定的課程
        top_students_by_course = []
        for course in all_courses:
            students = Classmate.objects.filter(classnumber__coursenumber=course.coursenumber).order_by('-score')[:10]
            top_students_by_course.append((course, enumerate(students, 1)))  # 包含學生的排名信息

    context = {
        'all_courses': all_courses,
        'top_students_by_course': top_students_by_course,
        'selected_course_number': selected_course_number,
    }
    return render(request, 'scores/honors.html', context)

def student_scorefind(request):
    classmates_query = Classmate.objects.filter(name=request.user).order_by("classdate")
    limit = 10
    paginator = Paginator(classmates_query, limit)
    page = request.GET.get('page', 1)
    try:
        classmates = paginator.page(page)  
    except PageNotAnInteger: 
        classmates = paginator.page(1) 
    except EmptyPage:  
        classmates = paginator.page(paginator.num_pages)
    context = {
        'classmates': classmates,
    }
    return render(request, 'scores/student-grades.html', context)

def admin_scorefind(request,course_number):
    
    classmates_name = request.GET.get('name')
    classmates_all = Classmate.objects.filter(classnumber__coursenumber=course_number).order_by('classdate')
    course_name = classmates_all.first().classnumber.coursename

    limit = 10
    paginator = Paginator(classmates_all, limit)
    page = request.GET.get('page', 1)
    try:
        classmates = paginator.page(page)  
    except PageNotAnInteger: 
        classmates = paginator.page(1) 
    except EmptyPage:  
        classmates = paginator.page(paginator.num_pages)

    num_classmates = classmates_all.count()
    context = {
        'name': classmates_name,
        'number': course_number,
        'classmates': classmates,
        'num_classmates': num_classmates,
        'course_name': course_name,
    }
    return render(request, 'scores/student-grades.html', context)


def admin_coursefind(request):
    all_courses = Course.objects.all().order_by("coursenumber").order_by('start_date')
    num_courses = all_courses.count()
    
    limit = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(all_courses, limit)
    try:
        courses = paginator.page(page)  
    except PageNotAnInteger: 
        courses = paginator.page(1) 
    except EmptyPage:  
        courses = paginator.page(paginator.num_pages)
    
    def filter_courses_by_date_range(courses, start_date, end_date):
        # 根据传入的起始日期和结束日期筛选课程
        return courses.filter(start_date__gte=start_date, start_date__lte=end_date)
    
    selected_startdate = request.GET.get('startdate')
    selected_enddate = request.GET.get('enddate')
    courses = all_courses

    if selected_startdate and selected_enddate:
        # 将日期字符串转换为日期对象
        start_date = datetime.strptime(selected_startdate, '%Y-%m-%d')
        end_date = datetime.strptime(selected_enddate, '%Y-%m-%d')
        # 使用筛选函数根据日期筛选课程
        courses = filter_courses_by_date_range(all_courses, start_date, end_date)

    context = {
        'courses': courses,
        'num_courses': num_courses,
    }

    return render(request, 'scores/score_find.html', context)

def add(request):
    if request.method == "POST":

        course_name = request.POST.get('course_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        course_img = request.FILES.get('course_image')
        introduce = request.POST.get('introduce')
        course = Course(coursename=course_name,start_date=start_date,end_date=end_date, course_image=course_img, introduce=introduce)
        course.save()
        return render(request, 'scores/add.html', locals())

    return render(request, 'scores/add.html', locals())

from datetime import datetime

def detail(request):
    list_course = Course.objects.all().order_by("coursenumber")

    def filter_courses_by_date_range(courses, start_date, end_date):
        # 根据传入的起始日期和结束日期筛选课程
        return courses.filter(start_date__gte=start_date, start_date__lte=end_date)
    
    selected_startdate = request.GET.get('startdate')
    selected_enddate = request.GET.get('enddate')

    if selected_startdate and selected_enddate:
        # 将日期字符串转换为日期对象
        start_date = datetime.strptime(selected_startdate, '%Y-%m-%d')
        end_date = datetime.strptime(selected_enddate, '%Y-%m-%d')
        # 使用筛选函数根据日期筛选课程
        list_course = filter_courses_by_date_range(list_course, start_date, end_date)

    limit = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(list_course, limit)
    try:
        list_course_page = paginator.page(page)  
    except PageNotAnInteger: 
        list_course_page = paginator.page(1) 
    except EmptyPage:  
        list_course_page = paginator.page(paginator.num_pages)

    context = {
        'list_course': list_course_page,
    }

    return render(request, 'scores/course-list.html', context)


def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        # 先抓取圖片位置，再刪除資料庫資料
        course_img = course.course_image
        course_img.delete(save=False)
        course.delete()
        return redirect('course:detail') 
    return render(request, 'course/course-list.html', {'course': course})

def analysis_chart(request):
    course_number = request.GET.get('coursenumber')
    classmates = Classmate.objects.filter(classnumber__coursenumber=course_number)


    num_classmates = classmates.count()
    context = {
        'number': course_number,
        'classmates': classmates,
        'num_classmates': num_classmates,
    }
    return render(request, 'scores/analysis_chart.html', context)


def training_result(request):
    training_number = request.GET.get('coursenumber')

    trainings = TrainingResult.objects.filter(course_id=training_number)
    num_vents = trainings.count()
    training_list = []

    for training in trainings:
        training.events = json.loads(training.events)
        training_result = TrainingResult.objects.get(pk=training.pk)
        course_name = training.course_name  # 提取课程名称
        event_query_set = EventResult.objects.filter(training_id=training_result)
        training_list.append((training, event_query_set,course_name))  # 將訓練結果和事件查詢集合添加到列表中

    context ={
        'trainings': trainings,
        'num_vents': num_vents,
        'training_list': training_list,
        'training_number': training_number,  # 将课程编号传递给模板
        'training_course_name':course_name,
    }
    return render(request, 'scores/training_result.html', context)

def training_result_user(request,course_number,train_pk):

    get_training_result = TrainingResult.objects.get(pk=train_pk)
    event_list = EventResult.objects.filter(training_id=get_training_result)
    for i in range(len(event_list)):
        envhour = int(event_list[i].time / 60)
        envsec = int(event_list[i].time % 60)
        event_list[i].time = "{hour:0{width}}:{sec:0{width}}".format(hour=envhour, sec=envsec, width=2)
    context = {
        'course_number': course_number,
        'event_list': event_list,
    }
    return render(request, 'scores/training_result_user.html', context)

def event_result(request):
    events =EventResult.objects.all()
    num_events = events.count()
    context ={
        'events':events,
        'num_events':num_events,
    }
    return render(request, 'scores/event_result.html', context)

import json
from random import randrange

from django.http import HttpResponse
from rest_framework.views import APIView

from pyecharts.charts import Bar, Pie, Funnel
from pyecharts import options as opts


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def bar_demo() -> Bar:
    Courses = Course.objects.all()
    # 分别儲存課程名稱和平均分數的列表
    Course_names = [course.coursename for course in Courses]
    Avg_scores = [round(course.Avg_score, 1) for course in Courses]
    Median_score = [course.Median_score for course in Courses]

# 创建长条图
    c = (
        Bar()
        .add_xaxis(Course_names)
        .add_yaxis("平均分數", Avg_scores)
        .add_yaxis("中位數", Median_score)
        .set_colors(["orange", "pink", "orange", "red", "green", "blue", "purple"])
        .dump_options_with_quotes()
    )
    return c


def bar_demo2(course_number) -> Bar:
    # 根据课程编号过滤 Classmate 对象
    classmates = Classmate.objects.filter(classnumber__coursenumber=course_number)
    
    # 分别儲存學生名稱和成績的列表
    student_names = [classmate.name.username for classmate in classmates]
    scores = [classmate.score for classmate in classmates]

    # 创建长条图
    c = (
        Bar()
        .add_xaxis(student_names)
        .add_yaxis("成績", scores)
        .set_colors(["orange", "pink", "orange", "red", "green", "blue", "purple"])
        .dump_options_with_quotes()
    )
    return c



from django.db.models import Count, F
def bar_demo3() -> Bar:
# 查询每个 event_id 的次数
    event_counts = EventResult.objects.values('event_id').annotate(count=Count('event_id'))

    # 获取 event_id 和对应的次数
    event_ids = [event['event_id'] for event in event_counts]
    counts = [event['count'] for event in event_counts]

    # 创建长条图
    c = (
        Bar()
        .add_xaxis(event_ids)
        .add_yaxis("次数", counts)
        .set_colors(["orange", "pink", "orange", "red", "green", "blue", "purple"])
        .dump_options_with_quotes()
    )
    return c


def pie_demo() -> Pie:
    Courses = Course.objects.all()
    # 分别儲存課程名稱和平均分數的列表
    Course_names = [course.coursename for course in Courses]
    Avg_scores = [round(course.Avg_score, 1) for course in Courses]

    context = {
        'Courses': Courses,
        'Course_names':Course_names,
        'Avg_scores': Avg_scores,
    }
    #pdb.set_trace()
    ddd = (
        Pie()
        .add("", [list(z) for z in zip(Course_names, Avg_scores)])
        .set_colors(["blue", "green", "orange", "red", "pink", "orange", "purple"])
        .set_global_opts(title_opts=opts.TitleOpts(title="課程平均分數佔比"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .dump_options_with_quotes() #將圖表中所有設置導出為json 格式
    )
    return ddd

class ChartView(APIView):
     def get(self, request, *args, **kwargs):
        course_number = request.GET.get('coursenumber')  # 获取课程编号
        print("Received course number:", course_number)  # 打印接收到的课程编号参数
        chart_data = bar_demo2(course_number)  # 调用 bar_demo2 函数并传递课程编号参数
        return JsonResponse(chart_data)

class Event_ChartView(APIView):
    def get(self, request, *args, **kwargs):
        # 调用 bar_demo3 函数生成长条图表数据
        chart_data = bar_demo3()
        return JsonResponse(chart_data)
    
def bar_demo4(training_courseid):
    # 获取特定课程的训练结果
    trainings = TrainingResult.objects.filter(course_id=training_courseid)
    
    # 获取特定课程中每个事件的发生次数
    event_counts = EventResult.objects.filter(training_id__in=trainings).values('event_name').annotate(count=Count('id'))


    # 提取事件名称和对应的次数
    event_names = [event['event_name'] for event in event_counts]
    counts = [event['count'] for event in event_counts]

    # 创建长条图
    c = (
        Bar()
        .add_xaxis(event_names)
        .add_yaxis("次数", counts)
        .set_colors(["orange", "pink", "orange", "red", "green", "blue", "purple"])
        .dump_options_with_quotes()
    )
    return c

class Training_ChartView(APIView):
    def get(self, request, *args, **kwargs):
        training_courseid = request.GET.get('coursenumber')

# 检查课程编号是否为空
        if training_courseid is None:
            return JsonResponse({"error": "Missing course number"}, status=400)
        
        # 调用 bar_demo3 函数生成长条图表数据
        chart_data = bar_demo4(training_courseid)
        return JsonResponse(chart_data)