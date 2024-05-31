from django.db import models

class Instructions(models.Model):
    instruction = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Инструкция Ассистенту")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Инструкция Ассистенту"
        verbose_name_plural = "Инструкция Ассистенту"
        ordering = ['-uploaded_at']  # Add default ordering

    def __str__(self):
        return str(self.uploaded_at)
