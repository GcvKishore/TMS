from django import forms
from django.forms import ModelForm
from .models import *


class MakeExamForm(ModelForm):
    title = forms.CharField(max_length=124)
    subject = forms.CharField(max_length=64)
    level = forms.CharField(max_length=64)
    date_time = forms.DateTimeField(required=False)
    duration = forms.DurationField(required=False)
    min_pass_points = forms.IntegerField(required=False)
    status = forms.CharField(required=False)
    username = forms.CharField(required=False)
    has_sections = forms.CharField()
    multiple_attempts = forms.CharField()

    class Meta:
        model = MakeExam
        fields = (
            'title', 'subject', 'level', 'date_time', 'duration', 'min_pass_points', 'has_sections',
            'multiple_attempts')
        exclude = ['owner', 'instructions']


class MakeQuestionForm(ModelForm):
    question_type = forms.CharField(max_length=64)
    max_time = forms.DurationField(required=False)
    max_points = forms.IntegerField(required=False)
    difficulty_level = forms.CharField(max_length=64, required=False)

    class Meta:
        model = MakeQuestion
        fields = ('question_type', 'question_text', 'max_time', 'max_points', 'difficulty_level')
        exclude = ['owner']


class MakeSectionForm(ModelForm):
    class Meta:
        model = MakeSection
        fields = ('title', 'sub_title', 'instructions', 'description')
        exclude = ['owner', 'exam']
