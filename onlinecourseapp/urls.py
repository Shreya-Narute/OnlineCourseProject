from django.urls import path

from . import views

app_name = "onlinecourseapp"

urlpatterns = [
    path(
        "courses/<int:course_id>/",
        views.course_details,
        name="course_details",
    ),
]
