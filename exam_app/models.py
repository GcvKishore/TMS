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
    max_time = models.DurationField(blank=True, null=True)
    max_points = models.IntegerField(blank=True, null=True)
    difficulty_level = models.CharField(max_length=64)
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
