
from .models import User, Vehicle, Ride
from django.conf import settings
from django.core.mail import send_mail


# helper to get driver's vehicle id by username
def get_vehicle(request):
    curr_user = User.objects.get(user_name=request.session["username"])
    if not curr_user.is_driver:
        return None
    return Vehicle.objects.get(driver_id=curr_user.id)


def send_mail_to_passenger(user):
    subject = 'Your ride has been confirmed'
    content = 'Dear ' + user.user_name + ' , your ride has been confirmed!\n' \
              + 'Please check on website for ride detail\n'
    send_mail(
        subject, content,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def modify_ride_status(ride, status):
    ride.status = status
    ride.save()
