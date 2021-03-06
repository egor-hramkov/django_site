# Generated by Django 4.0.5 on 2022-06-29 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='category',
        ),
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='news',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(verbose_name='Текст новости'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adout', models.TextField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='photos/user.png', null=True, upload_to='photos/')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
