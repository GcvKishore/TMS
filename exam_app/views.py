from django.shortcuts import render, redirect
from .forms import MakeExamForm, MakeQuestionForm
from .models import MakeExam, MakeQuestion, Option, Answer

# additional modules
from datetime import date


# Create your views here.
def createExam(request):
    if request.method == 'POST':
        make_exam_form = MakeExamForm(request.POST)
        if make_exam_form.is_valid():
            exam = make_exam_form.save()
            exam_id = exam.id
            return redirect('exam_app:edit-exam', exam_id)
        else:
            return render(request, 'exam_app/create-exam.html', {
                'error_message': "error occurred"
            })
    else:
        return render(request, 'exam_app/create-exam.html')


def editExam(request, exam_id):
    questions_list = MakeQuestion.objects.filter(exam_model__id=exam_id)
    exam_model = MakeExam.objects.get(id=exam_id)

    return render(request, 'exam_app/edit-exam.html', {
        'exam': exam_model,
        'questions': questions_list
    })


def addQuestion(request, exam_id):
    if request.method == 'POST':
        btn_action = request.POST['btn_action']
        make_question_form = MakeQuestionForm(request.POST)
        if make_question_form.is_valid():
            question = make_question_form.save()
            question.exam_model.add(exam_id)

            option_count = 0
            answer_count = 0
            for field in request.POST:
                if 'option' in field:
                    option_count += 1
                    text = request.POST[field]
                    option = Option.objects.create(option=text, question=question, index=option_count)
                    option.save()
                elif 'answer' in field:
                    answer_count += 1
                    text = request.POST[field]
                    answer = Answer.objects.create(answer=text, question=question, index=answer_count)
                    answer.save()

            if btn_action == 'add':
                return redirect('exam_app:add-question', exam_id)
            elif btn_action == 'save':
                print(btn_action)
                return redirect('exam_app:edit-exam', exam_id)
        else:
            print('error')
            return render(request, 'exam_app/add-question.html', {
                'exam_id': exam_id,
                'make_question_form': make_question_form,
            })
    else:
        return render(request, 'exam_app/add-question.html', {
            'exam_id': exam_id,
        })


def viewAllExamsInstructors(request):
    exams = MakeExam.objects.all()
    return render(request, 'exam_app/view-all-exams-instructor.html', {
        'exams': exams,
    })
