from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create/", views.create_page, name="create_page"),
    path("edit/<str:title>", views.edit, name="edit_page"),
    path("random/", views.random_page, name="random_page"),
    path("delete/<str:title>", views.delete_entry, name="delete_entry"),

]

