# Generated by Django 3.2.8 on 2021-11-22 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211102_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='duet_classes',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]