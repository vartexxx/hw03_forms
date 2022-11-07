"""Хранение моделей, для представления их из базы данных
"""
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    """Модель представления Группы(сообщества)
    имеет следующую структуру и ограничения:
    имя - tittle (длина не более 200 символов)
    адрес - slug (уникальное значение);
    описание - description
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Модель представления Постов(записей)
    имеет следующую стркутуру и ограничения:
    текс - text;
    дата публикации - pub_date(автоматически
    добавляется текущая дата);
    автор - author (ссылка на модель User)
    сообщество - group (ссылка на модель Group)"""
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.text

    # Класс Meta для упрощения сортировки по дате
    class Meta:
        ordering = ['-pub_date']
