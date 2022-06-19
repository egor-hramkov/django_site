from django.db import models
from django.urls import reverse

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False)
    category = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsById', kwargs={'news_id': self.pk})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})