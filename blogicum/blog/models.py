from django.contrib.auth import get_user_model
from django.db import models

import blog.constants as cnsts
from core.models import AbstractCreatedAt, AbstractIsPublishedCreatedAt

User = get_user_model()


class Category(AbstractIsPublishedCreatedAt):
    title = models.CharField('Заголовок', max_length=cnsts.MAX_CHAR_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:cnsts.MAX_STR_LENGTH]


class Location(AbstractIsPublishedCreatedAt):
    name = models.CharField(
        'Название места',
        max_length=cnsts.MAX_CHAR_LENGTH
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:cnsts.MAX_STR_LENGTH]


class Post(AbstractIsPublishedCreatedAt):
    title = models.CharField('Заголовок', max_length=cnsts.MAX_CHAR_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно делать '
                   'отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Фото',
        upload_to='Posts_images',
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:cnsts.MAX_STR_LENGTH]


class Comment(AbstractCreatedAt):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta(AbstractCreatedAt.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:cnsts.MAX_STR_LENGTH]
