# Generated by Django 4.1 on 2022-08-28 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_rename_following_user_id_userfollowing_following_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
