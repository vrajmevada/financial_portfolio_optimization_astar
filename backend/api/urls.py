from django.urls import path
from .views import optimize_api

urlpatterns = [
    path("optimize/", optimize_api),
]
