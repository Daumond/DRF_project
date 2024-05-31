from django.urls import path, include
from rest_framework import routers

from course.views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lessons-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lessons-detail')
]