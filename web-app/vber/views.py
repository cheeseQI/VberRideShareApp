
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .util import *

from django.db.models import Q

from .models import User, Vehicle, Ride
from django.shortcuts import get_list_or_404, render
from django.urls import reverse


# use to check system health
def index(request):
    return HttpResponse("Hello, world. You're at the vber index.")


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
    # todo: only user for test!
    request.session["username"] = "test_user"
    curr_user = User.objects.get(user_name=request.session["username"])
    dest = request.POST.get('dest')
    e_time = request.POST.get('earliest_arrival_time')
    l_time = request.POST.get('latest_arrival_time')
    ride_list = list(Ride.objects.filter(status='open', dest_addr=dest, required_time__range=(e_time, l_time))
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





