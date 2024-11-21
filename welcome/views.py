from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Account
from django.contrib import messages

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    print(username)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/home/')

    else:
        return render(request, 'welcome/login.html', locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/home/')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    u_names = request.POST.get('u_name', '')
    phone_number = request.POST.get('phone_number', '')
    email = request.POST.get('email', '')
    position = request.POST.get('position', '')
    company = request.POST.get('company', '')
    eor = []
    if len(User.objects.filter(username=username)) == 0 and username != '':
        new_user = User.objects.create(username=username, password=password)
        new_user.set_password(password)
        new_user.is_staff = False
        new_user.save()
        auth.login(request, new_user)
        if phone_number == "":
            phone_number = None
        NEW_Account = Account(userID=new_user, u_name=u_names,phone_number=phone_number,email=email,company=company,position=position)
        NEW_Account.save()
        return HttpResponseRedirect('/home/')
    elif username == '':
        eor.append('')
    else:
        eor.append("提示：此帳號已被使用。")
    context = {'eor': eor}

    return render(request, 'welcome/register.html', context)



