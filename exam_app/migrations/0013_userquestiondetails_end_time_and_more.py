# Generated by Django 4.0.3 on 2022-04-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0012_makequestion_evaluation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestiondetails',
            name='end_time',
            field=models.TimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='userquestiondetails',
            name='start_time',
            field=models.TimeField(default=None, null=True),
        ),
    ]
