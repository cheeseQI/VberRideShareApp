
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .util import *

from django.db.models import Q

from .models import User, Vehicle, Ride
from django.shortcuts import get_list_or_404, render
from django.urls import reverse

from django.shortcuts import render,redirect
from . import models
from .forms import UserForm


# use to integerate main functions, the entry page of the website (after login)
def main_page(request):
    return render(request, 'vber/main_page.html')


# the driver can search for open ride that fit vehicle and passenger number
def ride_search_by_driver(request):
    vehicle = get_vehicle(request)
    if vehicle is None:
        return render(request, 'vber/wait_and_redirect.html')
    ride_list = list(Ride.objects.filter(status='open', spec_info=vehicle.spec_info, vehicle_type=vehicle.type))
    # filter number exceed the limit
    r_ids = [r.id for r in ride_list if r.get_total_passenger() <= vehicle.max_capacity]
    ride_list = Ride.objects.filter(id__in=r_ids)
    context = {'ride_list': ride_list}
    return render(request, 'vber/driver_search.html', context)


# the sharer can search for open ride that fit destination, arrival time window, and passenger number
def ride_search_by_sharer(request):
    return render(request, 'vber/sharer_search.html')


# the sharer can search for open ride that fit destination, arrival time window, and passenger number
def show_ride_search_result_by_sharer(request):
    curr_user = User.objects.get(user_name=request.session["username"])
    dest = request.POST.get('dest')
    e_time = request.POST.get('earliest_arrival_time')
    l_time = request.POST.get('latest_arrival_time')
    ride_list = list(Ride.objects.filter(status='open', dest_addr=dest, required_time__range=(e_time, l_time), can_share=True)
                     .exclude(owner_id=curr_user.id).exclude(Q(sharer__exact=curr_user)))
    number_in_party = request.POST.get('number_in_party')
    context = {'ride_list': ride_list, 'number_in_party': number_in_party}
    return render(request, 'vber/sharer_search_result.html', context)


def join_ride_by_sharer(request, ride_id, number_in_party):
    ride = Ride.objects.get(id=ride_id)
    curr_user = User.objects.get(user_name=request.session["username"])
    ride.sharer.add(curr_user)
    party_json = ride.number_in_party
    party_json[curr_user.user_name] = number_in_party
    print(party_json)
    ride.save()
    return HttpResponseRedirect(reverse('vber:sharer_search'))


# the driver can view the information of ride, including owner, sharer and their parties.
# he/she can also edit the ride status from open to confirmed
def ride_view_by_driver(request):
    vehicle = get_vehicle(request)
    if vehicle is None:
        return render(request, 'vber/wait_and_redirect.html')
    ride_list = list(Ride.objects.filter(vehicle_id=vehicle.id, status='confirmed'))
    context = {'ride_list': ride_list}
    return render(request, 'vber/driver_view.html', context)


def mark_complete_by_driver(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    modify_ride_status(ride, 'complete')
    return HttpResponseRedirect(reverse('vber:driver_view'))


def mark_confirmed_by_driver(request, ride_id):

    ride = Ride.objects.get(id=ride_id)
    modify_ride_status(ride, 'confirmed')
    owner = ride.owner
    send_mail_to_passenger(owner)
    for share in ride.sharer.all():
        send_mail_to_passenger(share)
    return HttpResponseRedirect(reverse('vber:driver_search'))


def request_ride(request):
    context = {'user_name':request.session["username"]}
    return render(request, 'vber/request_ride.html',context)


def request_ride_result(request):
    user = User.objects.get(user_name =  request.session["username"])
    can_share = True
    if(request.POST.get('can_share')=="False"):
        can_share = False
    dest = request.POST.get('dest_addr')
    vehicle_type = request.POST.get('vehicle_type')
    required_time = request.POST.get('required_time')
    status = 'open'
    number = request.POST.get('number')
    spec_info = request.POST.get('spec_info')
    number_in_party = {user.user_name:number}
    ride = Ride.objects.create(
        owner = user,
        can_share = True,
        dest_addr = dest,
        required_time = required_time,
        vehicle_type = vehicle_type,
        status = status,
        number_in_party = number_in_party,
        spec_info = spec_info
    )
    ride.save()
    context = {'ride':ride}
    return render(request, 'vber/request_ride_succeed.html', context)


def ride_request_editing_choose(request):
    user = User.objects.get(user_name =  request.session["username"])
    ride_list = Ride.objects.filter(status = 'open',owner = user)
    context = {'ride_list':ride_list,'user_name':request.session["username"]}
    return render(request, 'vber/ride_request_editing_choose.html', context)


def ride_request_editing_edit(request):
    ride = Ride.objects.get(id=request.POST.get('ride_id'))
    context = {'ride':ride,'user_name':request.session["username"]}
    return render(request, 'vber/ride_request_editing_edit.html', context)


def save_ride_editing(request,ride_id):
    ride = Ride.objects.get(id = ride_id)
    ride.can_share = request.POST.get('can_share')
    ride.dest_addr = request.POST.get('dest_addr')
    ride.required_time = request.POST.get('required_time')
    ride.vehicle_type = request.POST.get('vehicle_type')
    ride.number = request.POST.get('number')
    ride.spec_info = request.POST.get('spec_info')
    
    ride.save()
    return HttpResponseRedirect(reverse('vber:main_page'))


def ride_status_viewing_choose(request):
    user = User.objects.get(user_name =  request.session["username"])
    all_ride = Ride.objects.all()
    ride_list = []
    for ride in all_ride:
        if ride.owner == user:
            ride_list.append(ride)
            continue
        for sharer in ride.sharer.all():
            if sharer == user:
                ride_list.append(ride)
    context = {'ride_list':ride_list,'user_name':request.session["username"]}
    return render(request, 'vber/ride_status_viewing_choose.html', context)

def ride_status_viewing_detail(request):
    user = User.objects.get(user_name =  request.session["username"])
    ride = Ride.objects.get(id = request.POST.get('ride_id'))
    context = {'ride':ride,'user_name':request.session["username"]}
    return render(request, 'vber/ride_status_viewing_detail.html', context)
    return render(request, 'login/index.html')


def login(request):
    loginHtml = 'login/login.html'
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(user_name = username)
            except:
                message = 'no such user'
                print('123131')
                return render(request, loginHtml, locals())

            if(user.password == password):
                user.is_login = True
                request.session['userid'] = str(user.pk)
                request.session['username'] = user.user_name
                return HttpResponseRedirect(reverse('vber:main_page'))
            else:
                message = "wrong password"
                return render(request, loginHtml, locals())
        else:
            return render(request, loginHtml, locals())

    login_form = UserForm()
    return render(request, loginHtml, locals())    


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # user = models.User.objects.create_user(user_name = username, email = email, password = password)
        user = models.User()
        user.user_name = username
        user.email = email
        user.password = password
        user.save()
        return HttpResponseRedirect(reverse('vber:login'))
    return render(request,'login/register.html')


def driverRegister(request):
    user = models.User.objects.get(pk=request.session['userid'])
    if user.is_driver == True:
        return HttpResponseRedirect(reverse('vber:driverEdit'))
    if request.method == "POST":
        user.is_driver = True
        driver_name = request.POST.get('driver_name')
        type = request.POST.get('type')
        plate_number = request.POST.get('plate_number')
        max_capacity = request.POST.get('max_capacity')
        spec_info = request.POST.get('spec_info')
        vehicle = models.Vehicle()
        vehicle.driver = user
        vehicle.driver_name = driver_name
        vehicle.type = type
        vehicle.plate_number = plate_number
        vehicle.max_capacity = max_capacity
        vehicle.spec_info = spec_info
        vehicle.save()
        user.save()
        return HttpResponseRedirect(reverse('vber:main_page'))
    return render(request, 'login/driverRegister.html')


def driverEdit(request):
    user = models.User.objects.get(pk=request.session['userid'])
    if user.is_driver == False:
        return HttpResponseRedirect(reverse('vber:driverRegister'))
    if request.method == 'POST':
        ##actually there should only be one vehicle for each 
        vehicles = models.Vehicle.objects.filter(driver = user)
        vehicle = vehicles[0]

        driver_name = request.POST.get('driver_name')
        type = request.POST.get('type')
        plate_number = request.POST.get('plate_number')
        max_capacity = request.POST.get('max_capacity')
        spec_info = request.POST.get('spec_info')  
        vehicle.driver_name = driver_name
        vehicle.type = type
        vehicle.plate_number = plate_number
        vehicle.max_capacity = max_capacity
        vehicle.spec_info = spec_info
        vehicle.save()
        return HttpResponseRedirect(reverse('vber:main_page'))
    return render(request, 'login/driverEdit.html')


def ridePage(request, user_id, ride_id):
     user = models.User.objects.get(pk = user_id)
     ride = models.Ride.objects.get(pk = ride_id)
     return render(request, 'login/ridePage.html', locals())


def logout(request):
    pass
    return redirect('/index/')
