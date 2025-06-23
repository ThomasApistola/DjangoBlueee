from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('hello/', views.say_hello, name="hello"),
    path("", include("django.contrib.auth.urls")),
]