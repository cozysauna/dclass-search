# Generated by Django 3.2.8 on 2021-11-18 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dclass_application', '0008_classes_comment_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='credict',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classes',
            name='num_student',
            field=models.IntegerField(default=0),
        ),
    ]
