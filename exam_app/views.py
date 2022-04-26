from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .functions import *
from datetime import datetime
from django.contrib.auth.models import User


# Create your views here.
@login_required
def createExam(request):
    if not request.user.is_staff:
        redirect('website:permission-denied')

    if request.method == 'POST':
        make_exam_form = MakeExamForm(request.POST)
        if make_exam_form.is_valid():
            exam = make_exam_form.save(commit=False)
            exam.owner = request.user
            exam.save()
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
                'title_error': '',
                'subject_error': '',
                'level_error': '',
                'date_error': '',
                'time_error': '',
                'duration_error': '',
                'min_pass_points_error': '',
                'has_sections_error': ''
            }
            for error in make_exam_form.errors:
                label = error + '_error'
                content[label] = make_exam_form.errors[error]
            return render(request, 'exam_app/instructor-create-exam.html', content)
    else:
        return render(request, 'exam_app/instructor-create-exam.html')


@login_required
def editExam(request, exam_id):
    exam = MakeExam.objects.get(id=exam_id)
    if not request.user.is_staff or exam.owner != request.user:
        redirect('website:permission-denied')

    if request.method == 'POST':
        if 'delete_question' in request.POST:
            delete_question_id = request.POST['delete_question']
            question = MakeQuestion.objects.get(id=delete_question_id)
            if question.owner == request.user:
                question.delete()

        if 'delete_section' in request.POST:
            delete_section_id = request.POST['delete_section']
            section = MakeSection.objects.get(id=delete_section_id)
            if section.owner == request.user:
                MakeQuestion.objects.filter(section__id=section.id).delete()
                section.delete()

        if 'publish-exam' in request.POST:
            exam = MakeExam.objects.get(id=exam_id)
            exam.status = 'Published'
            exam.save()

        if 'un-publish-exam' in request.POST:
            exam = MakeExam.objects.get(id=exam_id)
            exam.status = 'Draft'
            exam.save()

        if 'delete_exam' in request.POST:
            MakeQuestion.objects.filter(exam_model__id=exam_id).delete()
            MakeExam.objects.get(id=exam_id).delete()
            return redirect('exam_app:view-all-exams-instructors')

    questions_list = MakeQuestion.objects.filter(exam_model__id=exam_id)
    sections_list = MakeSection.objects.filter(exam=exam)
    return render(request, 'exam_app/instructor-edit-exam.html', {
        'exam': exam,
        'questions': questions_list,
        'sections': sections_list,
    })


@login_required
def addOptionsAnswers(request, question):
    if not request.user.is_staff:
        redirect('website:permission-denied')

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

    if question.max_points == 0 or question.max_points is None:
        question.max_points = answer_count
        question.save()

    return answer_count


@login_required
def addQuestion(request, exam_id):
    if not request.user.is_staff:
        redirect('website:permission-denied')

    if request.method == 'POST':
        btn_action = request.POST['btn_action']
        make_question_form = MakeQuestionForm(request.POST)
        if make_question_form.is_valid():
            question = make_question_form.save(commit=False)
            question.owner = request.user
            question.save()

            if question.question_type == 'Multiple Choice - Multiple Answers' or question.question_type == 'Fill In The Blanks':
                question.evaluation_type = True
            else:
                question.evaluation_type = False

            question.exam_model.add(exam_id)
            question.save()
            addOptionsAnswers(request, question)

            if question.max_points == 0 or question.max_points is None:
                question.max_points = 1
                question.save()

            if btn_action == 'add':
                return redirect('exam_app:add-question', exam_id)
            elif btn_action == 'save':
                return redirect('exam_app:edit-exam', exam_id)
        else:
            return render(request, 'exam_app/instructor-add-question.html', {
                'exam_id': exam_id,
                'make_question_form': make_question_form,
            })
    else:
        question_form = MakeQuestionForm()
        return render(request, 'exam_app/instructor-add-question.html', {
            'exam_id': exam_id,
            'question_form': question_form,
        })


@login_required
def viewAllExamsInstructors(request):
    if not request.user.is_staff:
        redirect('website:permission-denied')

    if request.method == 'POST':
        if 'publish' in request.POST:
            exam_id = request.POST['publish']
            exam = MakeExam.objects.get(id=exam_id)
            exam.status = 'Published'
            exam.save()

        if 'un-publish' in request.POST:
            exam_id = request.POST['un-publish']
            exam = MakeExam.objects.get(id=exam_id)
            exam.status = 'Draft'
            exam.save()

    exams = MakeExam.objects.filter(owner=request.user)
    return render(request, 'exam_app/instructor-view-all-exams.html', {
        'exams': exams,
    })


@login_required
def editExamDetails(request, exam_id):
    exam = MakeExam.objects.get(id=exam_id)
    if not request.user.is_staff or exam.owner != request.user:
        redirect('website:permission-denied')

    if request.method == 'POST':
        exam_form = MakeExamForm(request.POST, instance=exam)
        if exam_form.is_valid():
            details = exam_form.save(commit=False)
            details.owner = request.user
            details.save()
        return redirect("exam_app:edit-exam", exam_id=exam_id)
    return render(request, 'exam_app/instructor-edit-exam-details.html', {
        'exam': exam,
        'exam_duration': convertTimeString(str(exam.duration))
    })


@login_required
def EditQuestion(request, exam_id, question_id):
    question_model = MakeQuestion.objects.get(id=question_id)
    if not request.user.is_staff or question_model.owner != request.user:
        redirect('website:permission-denied')

    if request.method == 'POST':
        make_question_form = MakeQuestionForm(request.POST, instance=question_model)
        if make_question_form.is_valid():
            question = make_question_form.save(commit=False)
            question.max_points = request.POST['max_points']
            question.owner = request.user
            question.save()
            if question.question_type == 'Multiple Choice - Multiple Answers' or question.question_type == 'Fill In The Blanks':
                question.evaluation_type = True
            else:
                question.evaluation_type = False
            question.exam_model.add(exam_id)
            question.save()
            Option.objects.filter(question=question).delete()
            Answer.objects.filter(question=question).delete()
            addOptionsAnswers(request, question)
            if question.max_points == 0 or question.max_points is None:
                question.max_points = 1
                question.save()

    # End of post if exists

    question = MakeQuestion.objects.get(id=question_id)
    option_objects = Option.objects.filter(question=question)
    answer_objects = Answer.objects.filter(question=question)
    question_form = MakeQuestionForm(instance=question)
    options = Option.objects.filter(question=question).values_list('option', flat=True)
    answers = Answer.objects.filter(question=question).values_list('answer', flat=True)
    return render(request, 'exam_app/instructor-edit-question.html', {
        'exam_id': exam_id,
        'question': question,
        'options': options,
        'answers': answers,
        'question_duration': convertTimeString(str(question.max_time)),
        'question_form': question_form,
    })


@login_required
def viewAllExamsTutee(request):
    if request.user.is_staff:
        return redirect('exam_app:view-all-exams-instructors')
    exams = MakeExam.objects.filter(status='Published')
    return render(request, 'exam_app/tutee-view-all-exams.html', {
        'exams': exams,
    })


@login_required
def viewExam(request, exam_id):
    now = datetime.now()
    exam = MakeExam.objects.get(id=exam_id)
    username = request.user

    user_exam_details = UserExamDetails.objects.filter(username=username).exists()
    if user_exam_details:
        user_exam_details = UserExamDetails.objects.get(exam=exam.id, username=username)
    else:
        user_exam_details = UserExamDetails.objects.create(username=username, exam=exam, status='Yet To Take').save()
    return render(request, 'exam_app/tutee-view-exam.html', {
        'exam': exam,
        'user_exam_details': user_exam_details,
    })


@login_required
def viewAllDetails(request, exam_id):
    exam = MakeExam.objects.get(id=exam_id)
    student_exam_details = UserExamDetails.objects.filter(exam=exam)
    return render(request, 'exam_app/instructor-exam-results.html', {
        'student_exam_details': student_exam_details,
        'exam': exam,
    })


@login_required
def takeExam(request, exam_id, question_index):
    now = datetime.now()
    if request.method == 'POST':
        username = request.user
        btn_action = request.POST['btn_action']

        questions = MakeQuestion.objects.filter(exam_model__id=exam_id).order_by('pk')
        question = questions[question_index]

        exam_details = UserExamDetails.objects.get(exam=exam_id, username=username)

        question_details = UserQuestionDetails.objects.get(question=question, exam_details=exam_details,
                                                           username=username)
        question_details.end_time = now.strftime("%H:%M:%S")
        question_details.save()

        count = 0
        for user_input in request.POST:
            if 'answer' in user_input:
                count += 1
                user_answer = request.POST[user_input]
                UserAnswerTextInput.objects.filter(question=question_details, index=count,
                                                   username=username).delete()
                UserAnswerTextInput.objects.create(question=question_details, answer_text_input=user_answer,
                                                   index=count, username=username).save()

        for user_input in request.FILES:
            if 'user-upload' in user_input:
                count += 1
                file2 = request.FILES[user_input]
                UserAnswerFileUpload.objects.filter(question=question_details, index=count,
                                                    username=username).delete()
                UserAnswerFileUpload.objects.create(question=question_details, answer_text_input=file2,
                                                    index=count, username=username).save()

        if btn_action == 'next':
            question_index += 1
            return redirect('exam_app:takeExam', exam_id, question_index)
        elif btn_action == 'previous':
            question_index -= 1
            return redirect('exam_app:takeExam', exam_id, question_index)
        elif btn_action == 'quit':
            exam_details.status = 'Completed'
            exam_details.result_status = 'Pending'
            exam_details.end_time = now.strftime("%H:%M:%S")
            exam_details.save()
            return redirect('exam_app:exam-summary', exam_details.id)
        else:
            exam_details.status = 'Completed'
            exam_details.result_status = 'Pending'
            exam_details.end_time = now.strftime("%H:%M:%S")
            exam_details.save()
            return redirect('exam_app:exam-summary', exam_details.id)

    # Register user to the exams list
    username = request.user

    exam = MakeExam.objects.get(id=exam_id)
    status = "Ongoing"

    exam_details = UserExamDetails.objects.filter(exam=exam_id, username=username)
    if len(exam_details) == 0:
        UserExamDetails.objects.create(username=username, exam=exam, status=status,
                                       start_time=now.strftime("%H:%M:%S")).save()

    exam_details = UserExamDetails.objects.get(exam=exam_id, username=username)

    if question_index == 0:
        exam_details.start_time = now.strftime("%H:%M:%S")
        exam_details.save()

    # get exam object and linked questions(sorted)
    questions = MakeQuestion.objects.filter(exam_model__id=exam_id).order_by('pk')
    question = questions[question_index]

    # extract question details
    question_text = question.question_text
    options = Option.objects.filter(question=question.id)
    answers = Answer.objects.filter(question=question.id)

    if question.question_type == "Fill In The Blanks":
        question_text = generateFITB(question.question_text, answers)

    UserQuestionDetails.objects.filter(question=question, exam_details=exam_details, username=username).delete()
    UserQuestionDetails.objects.create(question=question, exam_details=exam_details, username=username,
                                       start_time=now.strftime("%H:%M:%S"))

    return render(request, 'exam_app/tutee-take-exam.html', {
        'exam': exam,
        'question': question,
        'question_text': question_text,
        'num_questions': len(questions) - 1,
        'options': options,
        'question_index': question_index,
        'question_number': question_index + 1,
    })


def takeExamSection(request, exam_id, section_index, question_index):
    now = datetime.now()

    # get exam, section, question details
    exam = MakeExam.objects.get(id=exam_id)
    sections = MakeSection.objects.filter(exam=exam).order_by('id')
    section = sections[section_index]
    questions = MakeQuestion.objects.filter(section=section).order_by('id')
    question = questions[question_index]

    # get user exam details
    username = request.user
    user_exam_details = UserExamDetails.objects.get(exam=exam, username=username)

    # Condition to check if the request method is post and if the thing can post
    # if request.method == 'POST' and user_exam_details.status == 'Ongoing':
    if request.method == 'POST':
        user_exam_details = UserExamDetails.objects.get(exam=exam, username=username)
        user_question_details = UserQuestionDetails.objects.get(username=username, question=question,
                                                                exam_details=user_exam_details)

        # Register time end time
        user_question_details.end_time = now.strftime("%H:%M:%S")
        user_question_details.save()

        count = 0
        for user_input in request.POST:
            if 'answer' in user_input:
                count += 1
                user_answer = request.POST[user_input]
                UserAnswerTextInput.objects.filter(question=user_question_details, index=count,
                                                   username=username).delete()
                UserAnswerTextInput.objects.create(question=user_question_details, answer_text_input=user_answer,
                                                   index=count, username=username).save()

        for user_input in request.FILES:
            if 'user-upload' in user_input:
                count += 1
                file2 = request.FILES[user_input]
                UserAnswerFileUpload.objects.filter(question=user_question_details, index=count,
                                                    username=username).delete()
                UserAnswerFileUpload.objects.create(question=user_question_details, answer_text_input=file2,
                                                    index=count, username=username).save()

        if "question_nav" in request.POST:
            question_index = request.POST['question_nav']
            return redirect('exam_app:take-exam-section', exam.id, section_index, question_index)

        btn_action = request.POST['btn_action']
        if btn_action == 'section_navigation':
            section_index = request.POST['section_nav_index']
            question_index = 0
            return redirect('exam_app:take-exam-section', exam.id, section_index, question_index)

        if btn_action == 'next':
            question_index += 1
            if question_index >= len(questions):
                question_index = 0
                section_index += 1
            if section_index >= len(sections):
                user_exam_details.status = 'Completed'
                user_exam_details.result_status = 'Pending'
                user_exam_details.end_time = now.strftime("%H:%M:%S")
                user_exam_details.save()
                return redirect('exam_app:exam-summary', user_exam_details.id)
            else:
                return redirect('exam_app:take-exam-section', exam.id, section_index, question_index)

        if btn_action == 'previous':
            question_index -= 1
            if question_index < 0:
                section_index -= 1
                current_section = sections[section_index]
                question_index = MakeQuestion.objects.filter(section=current_section).count() - 1
            return redirect('exam_app:take-exam-section', exam.id, section_index, question_index)

        if btn_action == 'finish' or btn_action == 'quit':
            user_exam_details.status = 'Completed'
            user_exam_details.result_status = 'Pending'
            user_exam_details.end_time = now.strftime("%H:%M:%S")
            user_exam_details.save()
            return redirect('exam_app:exam-summary', user_exam_details.id)

    # extract question text, options and answers
    question_text = question.question_text
    options = Option.objects.filter(question=question).values_list('option', flat=True)
    answers = Answer.objects.filter(question=question).values_list('answer', flat=True)

    # Check if question type is Fill in the blanks and change the answers to input tags
    if question.question_type == "Fill In The Blanks":
        question_text = generateFITB(question.question_text, answers)

    # change user exam status and register start time
    # if user_exam_details.status == 'Yet To Take':
    if question_index == 0 and section_index == 0:
        user_exam_details.status = 'Ongoing'
        user_exam_details.start_time = now.strftime("%H:%M:%S")
        user_exam_details.save()

    # get user question details
    user_question_details = UserQuestionDetails.objects.filter(username=username, question=question,
                                                               exam_details=user_exam_details).exists()
    if not user_question_details:
        UserQuestionDetails.objects.create(username=username, question=question, exam_details=user_exam_details,
                                           start_time=now.strftime("%H:%M:%S"))
    user_question_details = UserQuestionDetails.objects.get(username=username, question=question,
                                                            exam_details=user_exam_details)

    user_question_details.start_time = now.strftime("%H:%M:%S")
    user_question_details.save()

    return render(request, 'exam_app/tutee-take-exam-sections.html', {
        'exam': exam,
        'sections': sections,
        'section': section,
        'question': question,
        'section_index': section_index,
        'question_index': question_index,
        'options': options,
        'question_text': question_text,
    })


@login_required
def examSummary(request, exam_details_id):
    username = request.user
    exam_details = UserExamDetails.objects.get(id=exam_details_id)
    checkUserAnswers(request, exam_details)
    user_exam_details = UserExamDetails.objects.get(id=exam_details_id, username=username)
    return render(request, 'exam_app/tutee-exam-finish-summary.html', {
        'user_exam_details': user_exam_details,
    })


@login_required
def examResult(request, exam_details_id):
    checkEvaluationStatus(exam_details_id)
    username = request.user
    exam_details = UserExamDetails.objects.get(username=username, id=exam_details_id)
    exam_id = exam_details.exam_id
    exam = MakeExam.objects.get(id=exam_id)
    all_exam_questions_results = UserResults.objects.filter(exam_details=exam_details.id, username=username)
    return render(request, 'exam_app/tutee-exam-result-details.html', {
        'exam_details': exam_details,
        'all_exam_questions_results': all_exam_questions_results,
        'exam_details_id': exam_details_id,
        'exam_id': exam_id,
        'exam': exam,
    })


@login_required
def examResultsList(request, exam_id):
    username = request.user
    exam = MakeExam.objects.get(id=exam_id)
    exam_details = UserExamDetails.objects.filter(exam=exam_id, username=username)
    return render(request, 'exam_app/tutee-exam-results.html', {
        'all_exam_details': exam_details,
        'exam': exam,
    })


@login_required
def questionResult(request, exam_details_id, question_details):
    username = request.user

    user_question_details = UserQuestionDetails.objects.get(id=question_details, username=username)

    question_id = user_question_details.question_id
    question = MakeQuestion.objects.get(id=question_id)

    user_inputs = UserAnswerTextInput.objects.filter(question=user_question_details, username=username)

    user_uploads = UserAnswerFileUpload.objects.filter(question=user_question_details, username=username)

    exam_details = UserExamDetails.objects.get(id=exam_details_id)
    user_result = UserResults.objects.get(username=username, exam_details=exam_details,
                                          question_details=user_question_details, )

    return render(request, 'exam_app/tutee-question-result.html', {
        'question': question,
        'user_inputs': user_inputs,
        'user_uploads': user_uploads,
        'exam_details_id': exam_details_id,
        'user_question_details': user_question_details,
        'user_result': user_result,
    })


@login_required
def tuteeExamDetails(request, exam_id, exam_details_id):
    checkEvaluationStatus(exam_details_id)
    exam_details = UserExamDetails.objects.get(id=exam_details_id)
    exam = MakeExam.objects.get(id=exam_id)
    username = exam_details.username
    all_exam_questions_results = UserResults.objects.filter(exam_details=exam_details.id, username=username)
    return render(request, 'exam_app/instructor-user-exam-results.html', {
        'exam_details': exam_details,
        'all_exam_questions_results': all_exam_questions_results,
        'exam_details_id': exam_details,
        'exam': exam,
        'user_details': username,
    })


@login_required
def questionEvaluation(request, exam_details_id, question_details_id):
    exam_details = UserExamDetails.objects.get(id=exam_details_id)
    username = exam_details.username
    exam = exam_details.exam

    if request.method == 'POST':
        result = request.POST['result']
        remark = request.POST['remark']
        points = request.POST['points']

        user_question_details = UserQuestionDetails.objects.get(id=question_details_id)
        user_question_details.remark = remark
        user_question_details.evaluation_status = 'Evaluated'
        user_question_details.points = points

        user_result = UserResults.objects.get(username=username, exam_details=exam_details,
                                              question_details=user_question_details, )
        user_result.result = result
        user_question_details.evaluation_status = 'Evaluated'
        user_result.status = 'Evaluated'

        if result == 'Pending':
            user_question_details.evaluation_status = 'Pending'
            user_result.status = 'Pending'

        user_result.points = points
        user_result.save()
        user_question_details.save()
        # return redirect('exam_app:tutee-exam-results', exam.id, exam_details_id)

    user_question_details = UserQuestionDetails.objects.get(id=question_details_id)
    question_id = user_question_details.question_id
    question = MakeQuestion.objects.get(id=question_id)
    user_inputs = UserAnswerTextInput.objects.filter(question=user_question_details)
    user_uploads = UserAnswerFileUpload.objects.filter(question=user_question_details)
    user_result = UserResults.objects.get(username=username, exam_details=exam_details,
                                          question_details=user_question_details, )

    return render(request, 'exam_app/instructors-question-evaluation.html', {
        'question_details_id': question_details_id,
        'question': question,
        'user_inputs': user_inputs,
        'user_uploads': user_uploads,
        'exam_details_id': exam_details_id,
        'exam': exam,
        'user_question_details': user_question_details,
        'user_result': user_result,
    })


def addSection(request, exam_id):
    if not request.user.is_staff:
        redirect('website:permission-denied')

    exam = MakeExam.objects.get(id=exam_id)

    if request.method == 'POST':
        section_form = MakeSectionForm(request.POST)
        if section_form.is_valid():
            section = section_form.save(commit=False)
            section.owner = request.user
            section.exam = exam
            section.save()
            return redirect('exam_app:section-add-question', exam.id, section.id)
        else:
            return render(request, 'exam_app/instructor-add-section.html', {
                'exam': exam,
                'form': section_form,
            })

    form = MakeSectionForm()
    return render(request, 'exam_app/instructor-add-section.html', {
        'exam': exam,
        'form': form,
    })


def sectionAddQuestion(request, exam_id, section_id):
    if not request.user.is_staff:
        redirect('website:permission-denied')

    exam = MakeExam.objects.get(id=exam_id)
    section = MakeSection.objects.get(id=section_id)
    if request.method == 'POST':
        question_form = MakeQuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.owner = request.user
            if question.question_type == 'Multiple Choice - Multiple Answers' or question.question_type == 'Fill In The Blanks':
                question.evaluation_type = True
            else:
                question.evaluation_type = False

            if question.max_points == 0 or question.max_points is None:
                question.max_points = 1
            question.save()
            question.exam_model.add(exam.id)
            question.section.add(section.id)
            question.save()

            addOptionsAnswers(request, question)

            btn_action = request.POST['btn_action']
            if btn_action == 'next_question':
                return redirect('exam_app:section-add-question', exam.id, section.id)

            elif btn_action == 'save_exit':
                return redirect('exam_app:edit-exam', exam.id)

            elif btn_action == 'save_create_section':
                return redirect('exam_app:add-section', exam.id)
        else:
            return render(request, 'exam_app/instructor-add-question.html', {
                'exam': exam,
                'form': question_form,
                'section': section,
            })

    exam = MakeExam.objects.get(id=exam_id)
    section = MakeSection.objects.get(id=section_id)
    form = MakeQuestionForm()
    return render(request, 'exam_app/instructor-section-add-question.html', {
        'section': section,
        'exam': exam,
        'form': form,
    })


def editSection(request, exam_id, section_id):
    exam = MakeExam.objects.get(id=exam_id)
    section = MakeSection.objects.get(id=section_id)
    questions = MakeQuestion.objects.filter(section=section)

    if request.method == 'POST':
        if 'delete_question' in request.POST:
            delete_question_id = request.POST['delete_question']
            question = MakeQuestion.objects.get(id=delete_question_id)
            if question.owner == request.user:
                question.delete()
        elif 'btn-action' in request.POST:
            section_form = MakeSectionForm(request.POST, instance=section)
            if section_form.is_valid() and 'title' in request.POST:
                section = section_form.save(commit=False)
                if 'instructions' not in request.POST:
                    section.instructions = ''
                if 'description' not in request.POST:
                    section.description = ''
                section.save()
                if request.POST['btn-action'] == 'save_and_exit_section':
                    return redirect('exam_app:edit-exam', exam.id)

    section_form = MakeSectionForm(instance=section)
    return render(request, 'exam_app/instructor-edit-section.html', {
        'exam': exam,
        'section': section,
        'questions': questions,
        'form': section_form,
    })


def sectionEditQuestion(request, exam_id, section_id, question_id):
    exam = MakeExam.objects.get(id=exam_id)
    section = MakeSection.objects.get(id=section_id)
    question = MakeQuestion.objects.get(id=question_id)

    if not request.user.is_staff or question.owner != request.user:
        redirect('website:permission-denied')

    if request.method == 'POST':
        question_form = MakeQuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.max_points = request.POST['max_points']
            question.owner = request.user
            if question.question_type == 'Multiple Choice - Multiple Answers' or question.question_type == 'Fill In The Blanks':
                question.evaluation_type = True
            else:
                question.evaluation_type = False
            question.exam_model.add(exam_id)

            Option.objects.filter(question=question).delete()
            Answer.objects.filter(question=question).delete()
            addOptionsAnswers(request, question)

            if question.max_points == 0 or question.max_points is None:
                question.max_points = 1
            question.save()

    question_form = MakeQuestionForm(instance=question)
    options = Option.objects.filter(question=question).values_list('option', flat=True)
    answers = Answer.objects.filter(question=question).values_list('answer', flat=True)
    return render(request, 'exam_app/instructor-section-edit-question.html', {
        'form': question_form,
        'exam': exam,
        'section': section,
        'question': question,
        'options': options,
        'answers': answers,
        'question_duration': convertTimeString(str(question.max_time)),
    })
