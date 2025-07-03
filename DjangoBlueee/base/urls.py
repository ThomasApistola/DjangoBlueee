from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('password_change/', views.custom_password_change, name='password_change'),
    path("", include("django.contrib.auth.urls")),
    path("nameform/", views.nameform, name="nameform"),
    path("register/", views.register, name="register"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('collections/', views.user_collections, name='user_collections'),
    path('collections/<int:pk>/mark_collected/', views.mark_collected, name='mark_collected'),
    path('beheer/collections/', views.admin_collection_list, name='admin_collection_list'),
    path('beheer/collections/create/', views.create_collection, name='create_collection'),
    path('beheer/collections/<int:pk>/delete/', views.delete_collection, name='delete_collection'),
    path('beheer/collections/<int:pk>/approve/', views.approve_collection, name='approve_collection'),
    path('beheer/medicines/', views.medicine_list, name='medicine_list'),
    path('beheer/medicines/create/', views.create_medicine, name='create_medicine'),
    path('beheer/medicines/<int:pk>/edit/', views.edit_medicine, name='edit_medicine'),
    path('beheer/medicines/<int:pk>/delete/', views.delete_medicine, name='delete_medicine'),
    path('beheer/user/<int:user_id>/', views.user_profile_admin, name='user_profile_admin'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
]