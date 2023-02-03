from django.urls import path

from . import views

app_name = 'vber'
urlpatterns = [
    path('', views.index, name='index'),
    path('driver_view', views.ride_view_by_driver, name='driver_view'),
    path('driver_view/<int:ride_id>/mark_status_complete', views.mark_complete_by_driver, name='mark_status_complete'),
]