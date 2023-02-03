from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('driver_view', views.ride_view_by_driver, name='driver_view'),
]