from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect


from .models import User, Vehicle, Ride
from django.shortcuts import get_list_or_404, render
from django.urls import reverse
from django.core.mail import send_mail


def index(request):
    return HttpResponse("Hello, world. You're at the vber index.")


# the driver can search for open ride that fit vehicle and passenger information
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


# the driver can view the information of ride, including owner, sharer and their parties.
# he/she can also edit the ride status from open to confirmed
def ride_view_by_driver(request):
    vehicle = get_vehicle_by_driver(request)
    if vehicle is None:
        return HttpResponse("oh no, you are not the driver, no permission!")
    ride_list = list(Ride.objects.filter(vehicle_id=vehicle.id, status='confirmed'))
    context = {'ride_list': ride_list}
    return render(request, 'vber/driver_view.html', context)


# helper to get driver's vehicle id, todo:  to a util.py package
def get_vehicle_by_driver(request):
    # user for test!
    request.session["username"] = "test_user"
    # todo: need to verify the user valid or not first
    curr_user = User.objects.get(user_name=request.session["username"])
    if not curr_user.is_driver:
        return None
    return Vehicle.objects.get(driver_id=curr_user.id)


def mark_complete_by_driver(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 'complete'
    ride.save()
    return HttpResponseRedirect(reverse('vber:driver_view'))


def mark_confirmed_by_driver(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    ride.status = 'confirmed'
    ride.save()
    owner = ride.owner
    share_list = ride.sharer
    send_mail_to_passenger(owner)
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
