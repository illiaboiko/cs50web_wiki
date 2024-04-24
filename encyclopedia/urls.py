from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_article, name="article"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random"),
    path("create/", views.create, name="create"),\
    path("wiki/<str:title>/edit", views.edit, name="edit"),
]
