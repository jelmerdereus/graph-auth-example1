from django.urls import path

from . import views

urlpatterns = [
    # Home page
    path("", views.index, name="index"),

    # AUTH
    path("login", views.login_form, name="login"),
    path("logout", views.logout_link, name="logout"),

    # REST endpoints
    path("project_tasks", views.project_tasks, name="project_tasks"),
    path("own_project_tasks", views.own_project_tasks, name="own_project_tasks")
]
