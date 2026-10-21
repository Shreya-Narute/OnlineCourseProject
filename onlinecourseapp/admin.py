from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import Course, Lesson, Question, Choice, Submission


class ChoiceInline(StackedInline):
    model = Choice
    extra = 1


class QuestionInline(StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "course", "grade")
    search_fields = ("question_text",)


class LessonAdmin(ModelAdmin):
    list_display = ("title", "course")
    search_fields = ("title",)


class CourseAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.site_header = "OnlineCourse Administration"
admin.site.site_title = "OnlineCourse Admin"
admin.site.index_title = "OnlineCourse"

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
