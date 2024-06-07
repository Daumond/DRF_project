from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError

from course.models import Course, Lesson
from course.serializers import CourseSerializer, LessonSerializer
from user.permissions import IsNotModerator, IsOwnerOrModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        # создавать курсы может только пользователь, не входящий в группу модераторы
        if self.action == "create":
            permission_classes = [IsNotModerator]
        # редактировать курсы может только создатель курса или модератор
        elif self.action == "update" or self.action == "partial_update":
            permission_classes = [IsOwnerOrModerator]

        # удалять курсы может только их создатель
        elif self.action == "destroy":
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
