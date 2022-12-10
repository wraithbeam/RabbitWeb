from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sign-in/', views.sign_in, name="sign-in"),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('logout/', views.logout_user, name="logout"),
    path('new-meeting/', views.create_new_meeting, name='create-new-meeting'),
    path("<str:link>/", views.new_meeting, name="meeting"),
]
