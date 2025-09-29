from django.db import models
from django.conf import settings


class Post(models.Model):

    # Use AUTH_USER_MODEL to support the custom user model
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """
    Модель для комментариев к постам.
    """
    # Связь с постом: один пост - много комментариев
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,        # При удалении поста удаляем все комментарии
        related_name='comments',         # post.comments.all() - все комментарии поста
        verbose_name='Пост'
    )
    
    # Связь с автором комментария
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    
    # Текст комментария
    content = models.TextField(verbose_name='Текст комментария')
    
    # Дата создания комментария
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    

    def __str__(self):
        return f'Комментарий от {self.author} к посту "{self.post}"'

    class Meta:
        ordering = ['created_at']  # Сортировка комментариев от старых к новым
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    

