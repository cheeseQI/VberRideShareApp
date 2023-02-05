from django.urls import path
# from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^index/', views.index),
    # url(r'^login/', views.login),
    # url(r'^register/', views.register),
    # url(r'^logout/', views.logout),    
    path('index', views.index, name = 'index'),
    path('login', views.login),
    path('register', views.register),
    path('mainpage/<int:id>', views.mainpage, name = 'mainpage'),
    path('mainpage/<int:id>/driverRegister', views.driverRegister, name = 'driverRegister')
]