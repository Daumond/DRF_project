from django.db import models
from django.conf import settings

from user.models import User


NULLABLE = {"null": True, "blank": True}

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/previews/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "courses"
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="lessons/previews/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return f"{self.name} - {self.course}"

    class Meta:
        db_table = "lessons"
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь подписки', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс подписки', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='Актуальность')
    public_date = models.DateField(auto_now=True, verbose_name='Дата подписки', **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['public_date', 'course', 'user', ]
