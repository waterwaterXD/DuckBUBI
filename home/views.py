from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from welcome.models import Account
from django.contrib import messages



#@login_required  # 防止未登入者擅自進入
def index2(request):
    return render(request, 'home/index2.html', locals())

def student_information(request):
    user1 = Account.objects.get(userID=request.user)
    eor = []

    context = {'eor': eor,
               'user': user1}

    return render(request, 'home/student-information.html', context)






def student_revise(request):
    user1 = Account.objects.get(userID=request.user)
    u_names = request.POST.get('U-names', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    phone_number = request.POST.get('phone_number', '')
    position = request.POST.get('position', '')
    request.user.set_password(password)
    request.user.save()
    auth.login(request, request.user)
    user1.u_name = u_names
    user1.email = email
    if any(chr.isdigit() for chr in phone_number):
        user1.phone_number = phone_number
    user1.position = position
    user1.save()
    return HttpResponseRedirect('/home/student-information/')



from django.urls import reverse

def chatroom(request):
    return render(request, 'home/chatroom.html', )

def contact(request):
    return render(request, 'home/contact.html', )
def aboutus(request):
    return render(request, 'home/aboutus.html', )

def ebook(request):
    return render(request, 'home/ebook.html', )




from hospital.models import Hospital

def hospital(request):
    
    return render(request, 'home/hospital.html', )

def get_locations(request):
    counties = Hospital.objects.values('county').distinct()
    locations = {}
    for county in counties:
        districts = Hospital.objects.filter(county=county['county']).values('district').distinct()
        locations[county['county']] = [district['district'] for district in districts]

    return JsonResponse(locations)


def search_clinics(request):
    county = request.GET.get('county')
    district = request.GET.get('district')

    if county and district:
        clinics = Hospital.objects.filter(county=county, district=district)
        clinic_data = []
        for clinic in clinics:
            clinic_data.append({
                'name': clinic.name,
                'address': clinic.address,
                'phone': clinic.phone,
                'website': clinic.website,
                'photo_url': clinic.photo.url if clinic.photo else ''
            })
        return JsonResponse(clinic_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    

def video(request):
    return render(request, 'home/video.html', )
def questionnaire(request):
    return render(request, 'home/questionnaire.html', )


def depression(request):
    return render(request, 'home/depression.html', )
