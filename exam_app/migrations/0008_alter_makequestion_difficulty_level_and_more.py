# Generated by Django 4.0.3 on 2022-04-10 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0007_alter_makequestion_difficulty_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makequestion',
            name='difficulty_level',
            field=models.CharField(blank=True, default='', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='makequestion',
            name='max_points',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]