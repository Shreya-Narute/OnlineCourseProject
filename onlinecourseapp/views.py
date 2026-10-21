from django.shortcuts import get_object_or_404, render

from .models import Course


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        "onlinecourseapp/course_details_bootstrap.html",
        {"course": course},
    )
