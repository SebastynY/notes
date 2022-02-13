from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, )
    title = models.CharField(max_length=20)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Записка"
        verbose_name_plural = "Записки"

    def __str__(self):
        return self.title
