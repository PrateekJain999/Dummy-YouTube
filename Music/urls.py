from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    path("library/", views.library, name="library"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
]
