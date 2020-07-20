from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.entry_search, name="entry_search"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/<str:title>", views.view_entry, name="view_entry"),
    path("create", views.create_new_page, name="create_new_page")
]
