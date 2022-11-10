from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    """Модель представления Группы(сообщества)
    имеет следующую структуру и ограничения:
    имя - tittle (длина не более 200 символов)
    адрес - slug (уникальное значение);
    описание - description
    """
    title = models.CharField(max_length=200, verbose_name="Название группы")
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self) -> str:
        return str(self.title)


class Post(models.Model):
    """Модель представления Постов(записей)
    имеет следующую стркутуру и ограничения:
    текст - text;
    дата публикации - pub_date(автоматически
    добавляется текущая дата);
    автор - author (ссылка на модель User)
    сообщество - group (ссылка на модель Group)"""
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self) -> str:
        return str(self.text[:settings.CONST_TEXT])
