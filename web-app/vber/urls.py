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
    path('request_ride', views.request_ride, name='request_ride'),
    path('request_ride_result', views.request_ride_result, name='request_ride_result'),
    path('ride_request_editing_choose', views.ride_request_editing_choose, name='ride_request_editing_choose'),
    path('ride_request_editing_edit', views.ride_request_editing_edit, name='ride_request_editing_edit'),
    path('save_ride_editing/<int:ride_id>/save_ride', views.save_ride_editing, name='save_ride_editing'),
    path('ride_status_viewing_choose', views.ride_status_viewing_choose, name='ride_status_viewing_choose'),
    path('ride_status_viewing_detail', views.ride_status_viewing_detail, name='ride_status_viewing_detail')
]