from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import models
from .forms import UserForm
# def index(request):
#     return HttpResponse("Hello, world. You're at the vber index.")

def index(request):
    # if request.method == "POST":
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     print(username, password)
    #     return redirect('/index/')
    return render(request, 'login/index.html')

def mainpage(request, id):
    user = models.User.objects.get(pk = id)
    ##need to select open or confirmed rides
    ownerRides = []
    sharerRides = []
    ownerRidesTemp = models.Ride.objects.filter(owner = user)
    sharerRidesTemp = models.Ride.objects.filter(sharer = user)
    for o in ownerRidesTemp:
        if o.status == 'open' or o.status == 'confirmed':
            ownerRides.append(o)
    for s in sharerRidesTemp:
        if s.status == 'open' or s.status == 'confirmed':
            sharerRides.append(s)
    ##first search for all the vehicles this user have
    vehicles = models.Vehicle.objects.filter(driver = user)
    driverRides = []
    for vehicle in vehicles:
        driverrides = models.Ride.objects.filter(vehicle = vehicle)
        for d in driverrides:
            driverRides.append(d)
    # hasDriverRides = False
    # if len(driverRides) > 0:
    #     hasDriverRides = True 
    return render(request, 'login/mainpage.html', locals())

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
                return render(request, loginHtml, locals())
            
            if(user.password == password):
                user.is_login = True
                request.session['userid'] = str(user.pk)
                return redirect('mainpage', id = user.pk)
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
    return render(request,'login/register.html')

def driverRegister(request, id):
    if request.method == "POST":
        user = models.User.objects.get(pk = id)
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
    return render(request, 'login/driverRegister.html')

def driverEdit(request, id):
    if request.method == 'POST':
        user = models.User.objects.get(pk = id)
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
    return render(request, 'login/driverEdit.html')

def ridePage(request, user_id, ride_id):
     user = models.User.objects.get(pk = user_id)
     ride = models.Ride.objects.get(pk = ride_id)
     return render(request, 'login/ridePage.html', locals())

def logout(request):
    pass
    return redirect('/index/')