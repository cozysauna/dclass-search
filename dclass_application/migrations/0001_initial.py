# Generated by Django 3.2.8 on 2021-10-28 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_ratio', models.FloatField(default=0.0)),
                ('b_ratio', models.FloatField(default=0.0)),
                ('c_ratio', models.FloatField(default=0.0)),
                ('d_ratio', models.FloatField(default=0.0)),
                ('f_ratio', models.FloatField(default=0.0)),
                ('o_ratio', models.FloatField(default=0.0)),
                ('average_evaluation', models.FloatField(default=0.0)),
                ('term', models.CharField(max_length=100)),
                ('year', models.IntegerField(default=2021)),
                ('place', models.CharField(max_length=100)),
                ('class_form', models.CharField(max_length=100)),
                ('day', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('favorite', models.IntegerField(default=0)),
                ('textbook', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('faculty', models.CharField(max_length=100)),
                ('teacher', models.CharField(max_length=100)),
                ('syllabus_link', models.CharField(max_length=100)),
                ('test_ratio', models.IntegerField(default=0)),
                ('report_ratio', models.IntegerField(default=0)),
                ('participation_ratio', models.IntegerField(default=0)),
            ],
        ),
    ]
