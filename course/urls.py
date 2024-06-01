from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/', LessonListCreateAPIView.as_view(), name='lesson_list_create'),
    path('lesson/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson_retrieve_update_destroy'),

] + router.urls
