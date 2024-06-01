from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from course.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = SerializerMethodField()
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'description',
            'preview',
            'count_lessons',
            'lessons'
        )

    @staticmethod
    def get_count_lessons(course):
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons(course):
        return [lesson.__str__() for lesson in Lesson.objects.filter(course=course)]
