from django.urls import path
from . import views

urlpatterns = [
    path('new-participant', views.register_participant),
    path('get-winner', views.get_winner),
    path('create-password', views.create_password)
]
