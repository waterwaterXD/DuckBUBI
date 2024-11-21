from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, User, Questionnaire

# Create your views here.
def question_list(request):
    all_entries = Questionnaire.objects.all()
    context = {
        'questionnaires': all_entries,
    }
    return render(request, 'question/question_list.html', context)


def get_questionnaire(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
    questions = questionnaire.question_set.all()
    latest_question_list = questions.order_by('is_checkbox')[:]
    context = {
        'latest_question_list': latest_question_list,
        'title': questionnaire.title,
        'count': latest_question_list.count(),
    }
    return render(request, 'question/questionnaires.html', context)


def submit_vote(request):
    values = request.POST.items()
    q = User(pub_date=timezone.now())
    for k, v in values:
        if len(k) > 9 and k[:8] == 'question' and k[-2:] != '[]':
            question = get_object_or_404(Question, pk=int(k[9:]))
            try:
                selected_choice = question.choice_set.get(pk=int(v))
            except (KeyError, Choice.DoesNotExist):
                print("找不到")
            else:
                selected_choice.votes += 1
                selected_choice.save()
        elif len(k) > 9 and k[:8] == 'question' and k[-2:] == '[]':
            list = request.POST.getlist(k)
            question = get_object_or_404(Question, pk=int(k[9:11]))
            for value in list:
                try:
                    selected_choice = question.choice_set.get(pk=int(value))
                except (KeyError, Choice.DoesNotExist):
                    print("找不到")
                else:
                    selected_choice.votes += 1
                    selected_choice.save()
        else:
            q.__setattr__(k, v)
    q.save()
    return HttpResponseRedirect(reverse('question:question_list'))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'question/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('question:results', args=(question.id,)))
    

def analysis_chart(request):
    title = request.GET.get('title')  # 從請求中獲取標題
    questionnaire = Questionnaire.objects.filter(title=title)
    questions = Question.objects.all()

    context = {
        'title':title,
        'questionnaire':questionnaire,
        'questions':questions,
    }
    return render(request, 'question/question_analyis.html', context)





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


from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

def bar_demo() -> dict:
    Questions = Question.objects.all()
    Choices = Choice.objects.all()

    # 创建空列表来存储所有问题的选项及其对应的投票数
    all_data = []

    # 遍历每个问题
    for question in Questions:
        # 获取该问题的所有选项
        choices = Choices.filter(question=question)
        # 获取该问题的所有选项的文本和投票数
        choice_texts = [choice.choice_text for choice in choices]
        votes = [choice.votes for choice in choices]
        # 将选项及其对应的投票数组合成一个列表，并添加到 all_data 中
        all_data.append({"question_text": question.question_text, "choices": choice_texts, "votes": votes})

    # 创建 Bar 图
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(type_="value"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max"),
                    opts.MarkPointItem(type_="min", name="Min"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Average")]
            ),
        )
    )

    # 添加每个问题的所有选项及其对应的投票数到对应的 y 轴
    for data in all_data:
        x_axis_data = data["choices"]
        y_axis_data = data["votes"]
        c.add_xaxis(x_axis_data)
        c.add_yaxis(data["question_text"], y_axis_data)

    # 将图表对象转换为字典格式
    chart_data = c.dump_options_with_quotes()

    return chart_data





class Que_ChartView(APIView):
    def get(self, request, *args, **kwargs):
        # 调用 bar_demo3 函数生成长条图表数据
        chart_data = bar_demo()
        return JsonResponse(chart_data)



