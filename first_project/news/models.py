from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False)
    category = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title