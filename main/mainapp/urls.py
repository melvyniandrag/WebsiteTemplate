from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("create", views.create_view, name="create_view"),
    path("list", views.list_view, name="list_view"),
]
