from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('reserve_room/<int:room_id>/', views.reserve_room, name='reserve_room'),
    path('confirm_reservation/', views.confirm_reservation, name='confirm_reservation')
]