from django.urls import path

from . import views

app_name = 'vber'
urlpatterns = [
    path('', views.index, name='index'),
    path('driver_view', views.ride_view_by_driver, name='driver_view'),
    path('driver_view/<int:ride_id>/mark_status_complete', views.mark_complete_by_driver, name='mark_status_complete'),
    path('driver_search', views.ride_search_by_driver, name='driver_search'),
    path('driver_search/<int:ride_id>/mark_status_confirmed', views.mark_confirmed_by_driver, name='mark_status_confirmed'),
]