from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from course.models import Course, Lesson, Subscribe
from course.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from course.paginators import LessonPagination
from user.permissions import IsNotModerator, IsOwnerOrModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        permission_classes = [AllowAny]
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
    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]
    pagination_class = LessonPagination


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]
    pagination_class = LessonPagination


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
    pagination_class = LessonPagination


class SubscribeAPIView(APIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        new_sub = serializer.save()
        new_sub.user = self.request.user
        new_sub.save()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.kwargs['pk']
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscribe.objects.filter(user=user, course=course_item).first()

        # Если подписка у пользователя на этот курс есть - (де)/активируем ее
        if subs_item:
            if subs_item.is_active:
                subs_item.is_active = False
                subs_item.save()
                message = 'подписка деактивирована'
            else:
                subs_item.is_active = True
                subs_item.save()
                message = 'подписка активирована'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(user=user, course=course_item)
            message = 'подписка создана'
        # Возвращаем ответ в API
        return Response({"message": message})
