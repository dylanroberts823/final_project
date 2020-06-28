from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("create/", views.create_view, name="create"),
    path("manage/", views.manage_view, name="manage"),
    path("manage/<int:project_id>/", views.manage_project_view, name="manage_project"),
]
