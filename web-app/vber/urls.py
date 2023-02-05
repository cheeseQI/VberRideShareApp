from django.urls import path

from . import views

app_name = 'vber'
urlpatterns = [
    path('', views.index, name='index'),
    path('driver_view', views.ride_view_by_driver, name='driver_view'),
    path('driver_view/<int:ride_id>/mark_status_complete', views.mark_complete_by_driver, name='mark_status_complete'),
    path('driver_search', views.ride_search_by_driver, name='driver_search'),
    path('driver_search/<int:ride_id>/mark_status_confirmed', views.mark_confirmed_by_driver, name='mark_status_confirmed'),
    path('sharer_search', views.ride_search_by_sharer, name='sharer_search'),
    path('sharer_search_result', views.show_ride_search_result_by_sharer, name='sharer_search_result'),
    path('sharer_search_result/<int:ride_id>/<str:number_in_party>/join_ride_by_sharer', views.join_ride_by_sharer, name='join_ride'),
    path('request_a_new_ride/<str:dest_addr>/<int:vehicle_id>/<str:spec_info>/create_new_ride', views.request_a_new_ride, name='create_new_ride')
]