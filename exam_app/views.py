from django.shortcuts import render, redirect
from .forms import MakeExamForm, MakeQuestionForm
from .models import MakeExam, MakeQuestion, Option, Answer, UserExamDetails, UserQuestionDetails, \
    UserAnswerFileUpload, UserAnswerTextInput, UserResults
from .functions import checkUserAnswers
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


def viewAllExamsTutee(request):
    exams = MakeExam.objects.all()
    return render(request, 'exam_app/view-all-exams-tutee.html', {
        'exams': exams,
    })


def viewExam(request, exam_id):
    exam = MakeExam.objects.get(id=exam_id)
    return render(request, 'exam_app/view-exam.html', {
        'exam': exam,
    })


def generateFITB(question_text, answers):
    text = question_text
    for answer in answers:
        blank = "__________"
        text = text.replace(answer.answer, blank, 1)
    return text


def takeExam(request, exam_id, question_index):
    if request.method == 'POST':
        username = request.user.username

        questions = MakeQuestion.objects.filter(exam_model__id=exam_id).order_by('pk')
        question = questions[question_index]

        exam_details = UserExamDetails.objects.get(exam=exam_id, username=username)

        UserQuestionDetails.objects.filter(question=question, exam_details=exam_details).delete()
        question_details = UserQuestionDetails.objects.create(question=question, exam_details=exam_details)

        count = 0
        for user_input in request.POST:
            if 'answer' in user_input:
                count += 1
                user_answer = request.POST[user_input]
                print(user_answer)
                UserAnswerTextInput.objects.filter(question=question_details, index=count).delete()
                UserAnswerTextInput.objects.create(question=question_details, answer_text_input=user_answer,
                                                   index=count).save()

        btn_action = request.POST['btn_action']

        if btn_action == 'next':
            question_index += 1
            return redirect('exam_app:takeExam', exam_id, question_index)
        elif btn_action == 'previous':
            question_index -= 1
            return redirect('exam_app:takeExam', exam_id, question_index)
        else:
            exam_details.status = 'Completed'
            exam_details.result_status = 'Pending'
            exam_details.save()
            return redirect('exam_app:exam-summary', exam_details.id)

    # Register user to the exams list
    username = request.user.username
    exam = MakeExam.objects.get(id=exam_id)
    status = "Ongoing"

    exam_details = UserExamDetails.objects.filter(exam=exam_id, username=username)
    if len(exam_details) == 0:
        UserExamDetails.objects.create(username=username, exam=exam, status=status).save()

    # get exam object and linked questions(sorted)
    questions = MakeQuestion.objects.filter(exam_model__id=exam_id).order_by('pk')
    question = questions[question_index]

    # extract question details
    question_text = question.question_text
    options = Option.objects.filter(question=question.id)
    answers = Answer.objects.filter(question=question.id)

    if question.question_type == "Fill In The Blanks":
        question_text = generateFITB(question.question_text, answers)

    return render(request, 'exam_app/take-exam.html', {
        'exam': exam,
        'question': question,
        'question_text': question_text,
        'num_questions': len(questions) - 1,
        'options': options,
        'question_index': question_index,
        'question_number': question_index + 1,
    })


def examSummary(request, exam_details_id):
    checkUserAnswers(exam_details_id)
    user_exam_details = UserExamDetails.objects.get(id=exam_details_id)
    return render(request, 'exam_app/exam-summary.html', {
        'user_exam_details': user_exam_details,
    })


def examResult(request, exam_details_id):
    checkUserAnswers(exam_details_id)

    username = request.user.username
    exam_details = UserExamDetails.objects.get(username=username, id=exam_details_id)
    all_exam_questions_results = UserResults.objects.filter(exam_details=exam_details.id, username=username)
    return render(request, 'exam_app/exam-result.html', {
        'exam_details': exam_details,
        'all_exam_questions_results': all_exam_questions_results,
    })
