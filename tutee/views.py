from django.shortcuts import render
from exam_app.models import *
from datetime import timedelta
import datetime


# Create your views here.
def dashboard(request):
    today = datetime.datetime.now()
    five_hrs_back = today - datetime.timedelta(hours=5)
    mock_exams = MakeExam.objects.filter(multiple_attempts=True, status='Published')
    upcoming_exams = MakeExam.objects.filter(multiple_attempts=False, status='Published', date_time__gte=today)
    exams_list = MakeExam.objects.filter(multiple_attempts=False, status='Published', date_time__gte=five_hrs_back,
                                         date_time__lt=today)

    ongoing_exams = []
    for exam in exams_list:
        if (today - exam.duration) < exam.date_time:
            ongoing_exams.append(exam)

    return render(request, 'tutee/dashboard.html', {
        'mock_exams': mock_exams,
        'upcoming_exams': upcoming_exams,
        'ongoing_exams': ongoing_exams,
    })
