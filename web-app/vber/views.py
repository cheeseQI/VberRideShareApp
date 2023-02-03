from django.http import HttpResponse, Http404
from .models import User, Vehicle, Ride
from django.shortcuts import get_list_or_404, render


def index(request):
    return HttpResponse("Hello, world. You're at the vber index.")


# the rider can view the information of ride, including owner, sharer and their parties.
# he/she can also edit the ride status from open to confirmed
def ride_view_by_driver(request):
    # user for test!
    request.session["username"] = "test_user"
    # todo: need to verify the user valid or not first
    curr_user = User.objects.get(user_name=request.session["username"])
    if not curr_user.is_driver:
        return HttpResponse("shit, you are not the driver, no permission!")
    vehicle = Vehicle.objects.get(driver_id=curr_user.id)
    ride_list = list(Ride.objects.filter(vehicle_id=vehicle.id))
    context = {'ride_list': ride_list}
    return render(request, 'vber/driver_view.html', context)
