from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.entry_search, name="entry_search"),
    path("random_page", views.random_page, name="random_page"),
    path("wiki/<str:title>", views.view_entry, name="view_entry"),
    path("create", views.create_new_page, name="create_new_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page")
]
