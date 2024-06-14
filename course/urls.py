from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import (CourseViewSet, LessonListCreateAPIView, LessonListAPIView, LessonUpdateAPIView,
                          LessonRetrieveAPIView, LessonDestroyAPIView, SubscribeAPIView)

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create', LessonListCreateAPIView.as_view(), name='lesson_list_create'),
    path('lesson/list', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/<int:pk>/update', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/destroy', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
    path('subscribe/<int:pk>/', SubscribeAPIView.as_view(), name='subscribe'),


] + router.urls
