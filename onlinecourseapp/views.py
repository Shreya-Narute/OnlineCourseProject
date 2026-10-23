from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Choice, Course, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        "course_details_bootstrap.html",
        {"course": course},
    )


@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all() if hasattr(course, "questions") else Question.objects.filter(
        lesson__course=course
    )

    score = 0
    results = []

    for question in questions.prefetch_related("choices"):
        selected_choice_id = request.POST.get(f"choice_{question.id}")
        selected_choice = None

        if selected_choice_id:
            selected_choice = question.choices.filter(
                id=selected_choice_id
            ).first()

        is_correct = bool(
            selected_choice and selected_choice.is_correct
        )

        if is_correct:
            score += question.grade

        results.append(
            {
                "question": question,
                "selected_choice": selected_choice,
                "is_correct": is_correct,
                "correct_choice": question.choices.filter(
                    is_correct=True
                ).first(),
            }
        )

    request.session["exam_result"] = {
        "course_id": course.id,
        "course_name": course.name,
        "score": score,
        "total": sum(question.grade for question in questions),
        "results": [
            {
                "question": item["question"].question_text,
                "selected_choice": (
                    item["selected_choice"].choice_text
                    if item["selected_choice"]
                    else "Not answered"
                ),
                "correct_choice": (
                    item["correct_choice"].choice_text
                    if item["correct_choice"]
                    else "No correct answer configured"
                ),
                "is_correct": item["is_correct"],
            }
            for item in results
        ],
    }

    return redirect("onlinecourseapp:show_exam_result")


def show_exam_result(request):
    exam_result = request.session.get("exam_result")

    if not exam_result:
        return render(
            request,
            "exam_result.html",
            {"exam_result": None},
        )

    return render(
        request,
        "exam_result.html",
        {"exam_result": exam_result},
    )
