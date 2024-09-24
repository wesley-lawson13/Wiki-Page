from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("PageCreated", views.create_newpage, name="create_page"),
    path("newpage", views.new_page, name="new_page"),
    path("random", views.random, name="random"),
    path("Edit<str:title>", views.edit, name="edit"),
    path("<str:title>Updated", views.update_page, name="update_page"),
    path("<str:title>", views.entry, name="entry"),
    path("*search*", views.entry, name="search")
]
