from django.db import models

# Create your models here.
class Media(models.Model):
    audios = models.FileField(upload_to="audios/", verbose_name="Видео")
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    class Meta:
        verbose_name = "Медиа"
        verbose_name_plural = "Медиа"

    def __str__(self):
        return str(self.uploaded_at)
    
class RequestMedia(models.Model):
    audios = models.FileField(upload_to="audios/", verbose_name="Видео")
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    class Meta:
        verbose_name = "Медиа"
        verbose_name_plural = "Медиа"

    def __str__(self):
        return str(self.uploaded_at)