# Generated by Django 2.2.10 on 2020-05-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200424_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularpizza',
            name='image',
            field=models.ImageField(blank=True, upload_to='menu_image'),
        ),
    ]
