
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Course, Question, Submission


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

    questions = Question.objects.filter(
        lesson__course=course
    ).prefetch_related("choices")

    score = 0
    total = 0
    results = []
    last_submission = None

    for question in questions:
        total += question.grade

        selected_choice_id = request.POST.get(
            f"choice_{question.id}"
        )

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

        if selected_choice:
            last_submission = Submission.objects.create(
                question=question,
                choice=selected_choice,
                is_correct=is_correct,
            )

        correct_choice = question.choices.filter(
            is_correct=True
        ).first()

        results.append({
            "question": question.question_text,
            "selected_choice": (
                selected_choice.choice_text
                if selected_choice
                else "Not answered"
            ),
            "correct_choice": (
                correct_choice.choice_text
                if correct_choice
                else "No correct answer configured"
            ),
            "is_correct": is_correct,
        })

    request.session["exam_result"] = {
        "course_id": course.id,
        "course_name": course.name,
        "score": score,
        "total": total,
        "results": results,
    }

    if last_submission is not None:
        return redirect(
            "onlinecourseapp:show_exam_result",
            course_id=course.id,
            submission_id=last_submission.id,
        )

    return redirect(
        "onlinecourseapp:course_details",
        course_id=course.id,
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(
        Course,
        id=course_id,
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        question__lesson__course=course,
    )

    exam_result = request.session.get("exam_result")

    return render(
        request,
        "exam_result.html",
        {
            "course": course,
            "submission": submission,
            "exam_result": exam_result,
        },
    )
