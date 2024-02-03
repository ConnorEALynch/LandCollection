from django.urls import path
from . import views

urlpatterns = [
    # use query parameters to get and display cards
    path("", views.index, name="searchIndex"),
]