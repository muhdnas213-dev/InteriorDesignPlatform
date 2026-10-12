from django.contrib import admin
from django.urls import path

from mainapp import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Homepage
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),

    # Dashboards
    path(
        "client/dashboard/",
        views.client_dashboard,
        name="client_dashboard"
    ),

    path(
        "designer/dashboard/",
        views.designer_dashboard,
        name="designer_dashboard"
    ),
    path(
    "client/project/create/",
    views.create_project,
    name="create_project"
),
    path(
    "client/project/<int:project_id>/rooms/",
    views.room_details,
    name="room_details"
),
    path(
    "client/project/<int:project_id>/rooms/add/",
    views.add_room,
    name="add_room"
),
    path(
    "client/room/<int:room_id>/analyze/",
    views.analyze_room,
    name="analyze_room"
),
]