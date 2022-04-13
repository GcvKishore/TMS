# Generated by Django 4.0.3 on 2022-04-12 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MakeExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=124)),
                ('subject', models.CharField(max_length=64)),
                ('level', models.CharField(max_length=64)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('duration', models.DurationField(null=True)),
                ('min_pass_points', models.IntegerField(null=True)),
                ('status', models.CharField(blank=True, default='draft', max_length=64)),
                ('username', models.CharField(blank=True, default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='MakeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(max_length=64)),
                ('max_time', models.DurationField(null=True)),
                ('max_points', models.IntegerField(default=1, null=True)),
                ('difficulty_level', models.CharField(default='None', max_length=64, null=True)),
                ('evaluation_type', models.BooleanField(default=False)),
                ('exam_model', models.ManyToManyField(to='exam_app.makeexam')),
            ],
        ),
        migrations.CreateModel(
            name='UserExamDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('status', models.CharField(blank=True, max_length=64)),
                ('result_status', models.CharField(blank=True, max_length=64, null=True)),
                ('overall_points', models.IntegerField(blank=True, null=True)),
                ('start_time', models.TimeField(default=None, null=True)),
                ('end_time', models.TimeField(default=None, null=True)),
                ('time_elapsed', models.DurationField(null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.makeexam')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(blank=True, null=True)),
                ('evaluation_status', models.CharField(blank=True, max_length=64, null=True)),
                ('start_time', models.TimeField(default=None, null=True)),
                ('end_time', models.TimeField(default=None, null=True)),
                ('time_elapsed', models.DurationField(null=True)),
                ('exam_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.userexamdetails')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.makequestion')),
            ],
        ),
        migrations.CreateModel(
            name='UserResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('question_type', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=64)),
                ('result', models.CharField(max_length=64)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('time_elapsed', models.DurationField(null=True)),
                ('exam_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.userexamdetails')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.makequestion')),
                ('question_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.userquestiondetails')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswerTextInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text_input', models.TextField(blank=True, null=True)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.userquestiondetails')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswerFileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text_input', models.TextField(blank=True, null=True)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.userquestiondetails')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=124)),
                ('index', models.IntegerField(default=1)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.makequestion')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=124)),
                ('index', models.IntegerField(default=1)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_app.makequestion')),
            ],
        ),
    ]