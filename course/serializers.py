from rest_framework import serializers

from course.models import Course, Lesson
from user.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def get_count_lessons(self, obj: Course):
        return obj.lessons.all().count()


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    count_lessons = serializers.SerializerMethodField(read_only=True)

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

