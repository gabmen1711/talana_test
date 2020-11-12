from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Test project running"),
    path('new-participant', views.register_participant),
    path('get-winner', views.get_winner)
]
