from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class MakeExam(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=124)
    subject = models.CharField(max_length=64)
    level = models.CharField(max_length=64)
    date_time = models.DateTimeField(null=True)
    duration = models.DurationField(null=True)
    min_pass_points = models.IntegerField(null=True)
    status = models.CharField(max_length=64, blank=True, default='Draft')
    has_sections = models.BooleanField(default=False)
    multiple_attempts = models.BooleanField(default=False)
    instructions = RichTextUploadingField(blank=True, default="")

    def __str__(self):
        return self.title


class MakeSection(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=124, blank=True)
    sub_title = models.CharField(max_length=124, blank=True)
    instructions = RichTextUploadingField(blank=True, default="")
    description = RichTextUploadingField(blank=True, default="")
    exam = models.ForeignKey('MakeExam', blank=True, on_delete=models.CASCADE)


class MakeQuestion(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = RichTextUploadingField()
    question_type = models.CharField(max_length=64)
    max_time = models.DurationField(null=True)
    max_points = models.IntegerField(default=1)
    difficulty_level = models.CharField(max_length=64, default="None", null=True)
    exam = models.ManyToManyField('MakeExam')
    evaluation_type = models.BooleanField(default=False)
    section = models.ManyToManyField('MakeSection', default="", blank=True)

    def __str__(self):
        return self.question_type


class Option(models.Model):
    option = models.CharField(max_length=124)
    index = models.IntegerField(default=1)
    question = models.ForeignKey('MakeQuestion', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.option}-{self.index}"


class Answer(models.Model):
    answer = models.CharField(max_length=124)
    index = models.IntegerField(default=1)
    question = models.ForeignKey('MakeQuestion', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.answer}-{self.index}"


class UserExamDetails(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey('MakeExam', on_delete=models.CASCADE)
    status = models.CharField(max_length=64, default='Yet To Take')
    result_status = models.CharField(max_length=64, blank=True, null=True)
    overall_points = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(null=True, default=None)
    end_time = models.TimeField(null=True, default=None)
    time_elapsed = models.DurationField(null=True)
    date = models.DateTimeField(auto_now=True, null=True)


class UserQuestionDetails(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('MakeQuestion', on_delete=models.CASCADE)
    exam_details = models.ForeignKey('UserExamDetails', on_delete=models.CASCADE)
    points = models.IntegerField(blank=True, default=0)
    evaluation_status = models.CharField(max_length=64, blank=True, null=True)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)
    time_elapsed = models.DurationField(null=True)
    remark = models.TextField(default='', blank=True)


class UserAnswerTextInput(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('UserQuestionDetails', on_delete=models.CASCADE)
    answer_text_input = models.TextField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)


class UserAnswerFileUpload(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('UserQuestionDetails', on_delete=models.CASCADE)
    answer_text_input = models.FileField(null=True)
    index = models.IntegerField(blank=True, null=True)


@receiver(post_delete, sender=UserAnswerFileUpload)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.answer_text_input.delete(save=False)
    finally:
        pass


class UserResults(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=64)
    exam_details = models.ForeignKey('UserExamDetails', on_delete=models.CASCADE)
    question_details = models.ForeignKey('UserQuestionDetails', on_delete=models.CASCADE)
    question = models.ForeignKey('MakeQuestion', on_delete=models.CASCADE)
    status = models.CharField(max_length=64)
    result = models.CharField(max_length=64)
    points = models.IntegerField(blank=True, null=True)
    time_elapsed = models.DurationField(null=True)
