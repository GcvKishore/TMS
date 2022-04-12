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
            content = { 
                'title': request.POST['title'],
                'subject': request.POST['subject'],
                'level': request.POST['level'],
                'date': request.POST['date'],
                'time': request.POST['time'],
                'duration': request.POST['duration'],
                'min_pass_points': request.POST['min_pass_points'],
                'title_error':'',
                'subject_error':'',
                'level_error':'',
                'date_error':'',
                'time_error':'',
                'duration_error':'',
                'min_pass_points_error':'',
            }

            for error in make_exam_form.errors:
                label = error + '_error'
                content[label] = make_exam_form.errors[error]
            return render(request, 'exam_app/create-exam.html',content)
    else:
        return render(request, 'exam_app/create-exam.html')


def editExam(request, exam_id):
    questions_list = MakeQuestion.objects.filter(exam_model__id=exam_id)
    exam_model = MakeExam.objects.get(id=exam_id)

    return render(request, 'exam_app/edit-exam.html', {
        'exam': exam_model,
        'questions': questions_list
    })


def addOptionsAnswers(request, question):
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
            if question.question_type == 'Multiple Choice - Multiple Answers':
                correct_option = request.POST[field]
                text = request.POST[correct_option]
            answer = Answer.objects.create(answer=text, question=question, index=answer_count)
            answer.save()


def addQuestion(request, exam_id):
    if request.method == 'POST':
        btn_action = request.POST['btn_action']
        make_question_form = MakeQuestionForm(request.POST)
        if make_question_form.is_valid():
            question = make_question_form.save()
            question.exam_model.add(exam_id)

            addOptionsAnswers(request, question)

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


def editExamDetails(request,exam_id):
    examModel = MakeExam.objects.get(id=exam_id)
    if request.method == 'POST':   
        exam_form = MakeExamForm(request.POST,instance=examModel)
        if exam_form.is_valid():
            details = exam_form.save()
        return redirect("exam_app:edit-exam",exam_id=exam_id)

    return render(request, 'exam_app/edit-exam-details.html',{
        'exam_id':exam_id,
        'exam':examModel
    })



def EditQuestion(request, exam_id, question_id):
    if request.method == 'POST':
        question_model = MakeQuestion.objects.get(id=question_id)
        make_question_form = MakeQuestionForm(request.POST, instance=question_model)
        if make_question_form.is_valid():
            question = make_question_form.save()
            question.exam_model.add(exam_id)
            Option.objects.filter(question=question).delete()
            Answer.objects.filter(question=question).delete()
            print("Passed ")
            addOptionsAnswers(request, question)
            print("success")
        print("Failed")
    # End of post if exists

    question = MakeQuestion.objects.get(id=question_id)
    option_objects = Option.objects.filter(question=question)
    answer_objects = Answer.objects.filter(question=question)
    options = []
    answers = []
    for option in option_objects:
        options.append(option.option)
    for answer in answer_objects:
        answers.append(answer.answer)
    return render(request, 'exam_app/edit-question.html', {
        'exam_id': exam_id,
        'question': question,
        'options': options,
        'answers': answers,
    })
