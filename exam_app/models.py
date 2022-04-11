from django.db import models


class MakeExam(models.Model):
    title = models.CharField(max_length=124)
    subject = models.CharField(max_length=64)
    level = models.CharField(max_length=64)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    duration = models.DurationField(null=True)
    min_pass_points = models.IntegerField(null=True)
    status = models.CharField(max_length=64, blank=True, default='draft')
    username = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return self.title


class MakeQuestion(models.Model):
    question_text = models.TextField()
    question_type = models.CharField(max_length=64)
    max_time = models.DurationField(null=True)
    max_points = models.IntegerField(default=1, null=True)
    difficulty_level = models.CharField(max_length=64, default="None", null=True)
    exam_model = models.ManyToManyField('MakeExam')

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
    username = models.CharField(max_length=64)
    exam = models.ForeignKey('MakeExam', on_delete=models.CASCADE)
    status = models.CharField(max_length=64, blank=True)
    result_status = models.CharField(max_length=64, blank=True)
    overall_points = models.IntegerField(blank=True)
    time_elapsed = models.DurationField(null=True)


class UserQuestionDetails(models.Model):
    question = models.ForeignKey('MakeQuestion', on_delete=models.CASCADE)
    exam = models.ForeignKey('UserExamDetails', on_delete=models.CASCADE)
    points = models.IntegerField(blank=True)
    evaluation_status = models.CharField(max_length=64, blank=True)
    time_elapsed = models.DurationField(null=True)


class UserAnswerTextInput(models.Model):
    question = models.ForeignKey('UserQuestionDetails', on_delete=models.CASCADE)
    answer_text_input = models.TextField(blank=True)
    index = models.IntegerField(blank=True)


class UserAnswerFileUpload(models.Model):
    question = models.ForeignKey('UserQuestionDetails', on_delete=models.CASCADE)
    answer_text_input = models.TextField(blank=True)
    index = models.IntegerField(blank=True)
