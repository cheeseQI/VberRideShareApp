from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.utils.timezone import make_aware
from django.db.models import Q

from .models import User, Vehicle, Ride
from django.shortcuts import get_list_or_404, render
from django.urls import reverse
from django.core.mail import send_mail


def index(request):
    return HttpResponse("Hello, world. You're at the vber index.")


# the driver can search for open ride that fit vehicle and passenger number
def ride_search_by_driver(request):
    vehicle = get_vehicle_by_driver(request)
    if vehicle is None:
        return HttpResponse("oh no, you are not the driver, no permission!")
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
    ride_list = list(Ride.objects.filter(status='open', dest_addr=dest, required_time__range=(e_time, l_time))
                     .exclude(owner_id=curr_user.id).exclude(Q(sharer__exact=curr_user)))
    # todo: exclude sharer
    number_in_party = request.POST.get('number_in_party')
    context = {'ride_list': ride_list, 'number_in_party': number_in_party}
    return render(request, 'vber/sharer_search_result.html', context)


def join_ride_by_sharer(request, ride_id, number_in_party):
    ride = Ride.objects.get(id=ride_id)
    # todo: only user for test!
    request.session["username"] = "test_user"
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
    vehicle = get_vehicle_by_driver(request)
    if vehicle is None:
        return HttpResponse("oh no, you are not the driver, no permission!")
    ride_list = list(Ride.objects.filter(vehicle_id=vehicle.id, status='confirmed'))
    context = {'ride_list': ride_list}
    return render(request, 'vber/driver_view.html', context)


def mark_complete_by_driver(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 'complete'
    ride.save()
    return HttpResponseRedirect(reverse('vber:driver_view'))


# todo: abstract to util.py as a change_status(change_code, ride)
def mark_confirmed_by_driver(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 'confirmed'
    ride.save()
    owner = ride.owner
    send_mail_to_passenger(owner)
    for share in ride.sharer.all():
        send_mail_to_passenger(share)
    return HttpResponseRedirect(reverse('vber:driver_search'))


def send_mail_to_passenger(user):
    subject = 'Your ride has been confirmed'
    content = 'Dear ' + user.user_name + ' , your ride has been confirmed!\n' \
              + 'Please check on website for ride detail\n'
    # todo: unsafe! use other method(eg. token)
    send_mail(
        subject, content,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


# helper to get driver's vehicle id, todo:  to a util.py package
def get_vehicle_by_driver(request):
    # todo: only user for test!
    request.session["username"] = "test_user"
    # todo: need to verify the user valid or not first
    curr_user = User.objects.get(user_name=request.session["username"])
    if not curr_user.is_driver:
        return None
    return Vehicle.objects.get(driver_id=curr_user.id)

