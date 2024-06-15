from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from course.models import Course, Lesson, Subscribe
from course.validators import ValidatedUrl


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['is_active', 'user']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        validators = [ValidatedUrl(field='url'), ValidatedUrl(field='description')]
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = SerializerMethodField(read_only=True)
    count_lessons = SerializerMethodField(read_only=True)
    subscribe = SubscribeSerializer(read_only=True, source='subscribe_set', many=True)

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

    def get_subscribe(self, obj):
        return obj.subscribe_set.filter(user=self.request.user, course=obj).is_active

