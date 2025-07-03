from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path('hello/', views.say_hello, name="hello"),
    path("", include("django.contrib.auth.urls")),
    path("nameform/", views.nameform, name="nameform"),
    path("register/", views.register, name="register"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]