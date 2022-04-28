from .models import *
from datetime import datetime, date
import time


def validate_answers(user_answers, correct_answers, points):
    if len(user_answers) != len(correct_answers):
        return 'Incorrect', 0

    user_inputs = []
    for answer in user_answers:
        user_inputs.append(answer.answer_text_input.lower())

    answers = []
    for correct_answer in correct_answers:
        answers.append(correct_answer.answer.lower())

    for user_answer in user_inputs:
        if user_answer not in answers:
            return 'Incorrect', 0

    return 'Correct', points


def checkUserAnswers(request, exam_details):
    now = datetime.now()

    exam_details = UserExamDetails.objects.get(id=exam_details.id)

    username = exam_details.username
    exam = exam_details.exam
    questions = MakeQuestion.objects.filter(exam=exam).order_by('pk')

    for question in questions:
        if not UserQuestionDetails.objects.filter(question=question.id, exam_details=exam_details.id).exists():
            UserQuestionDetails.objects.create(question=question, exam_details=exam_details, username=request.user,
                                               start_time=now.strftime("%H:%M:%S"))
            question_details = UserQuestionDetails.objects.get(question=question, exam_details=exam_details,
                                                               username=request.user)
            question_details.end_time = now.strftime("%H:%M:%S")
            question_details.remark = "Didn't attend the question"
            question_details.save()

        user_question_details = UserQuestionDetails.objects.get(question=question.id,
                                                                exam_details=exam_details.id)
        start_time = user_question_details.start_time
        end_time = user_question_details.end_time

        if start_time and end_time:
            time_elapsed = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
            user_question_details.time_elapsed = time_elapsed
            user_question_details.save()

        if not question.evaluation_type or None:
            UserResults.objects.filter(username=username, exam_details=exam_details,
                                       question=question).delete()
            UserResults.objects.create(
                username=username,
                exam_details=exam_details,
                question_type=question.question_type,
                question=question,
                question_details=user_question_details,
                status='Pending',
                result='Pending',
                points=0,
                time_elapsed=user_question_details.time_elapsed
            ).save()
            user_question_details.evaluation_status = 'Pending'
            user_question_details.points = 0
        else:
            user_answers = UserAnswerTextInput.objects.filter(question=user_question_details.id)
            correct_answers = Answer.objects.filter(question=question.id)
            result, points = validate_answers(user_answers, correct_answers, question.max_points)
            UserResults.objects.filter(username=username, exam_details=exam_details,
                                       question=question).delete()
            UserResults.objects.create(
                username=username,
                exam_details=exam_details,
                question_type=question.question_type,
                question_details=user_question_details,
                question=question,
                status='Evaluated',
                result=result,
                points=points,
                time_elapsed=user_question_details.time_elapsed
            ).save()
            user_question_details.evaluation_status = 'Evaluated'
            user_question_details.points = points
        user_question_details.save()
    checkEvaluationStatus(exam_details.id)
    return


def checkEvaluationStatus(exam_details_id):
    exam_details = UserExamDetails.objects.get(id=exam_details_id)

    username = exam_details.username
    exam = exam_details.exam
    questions = MakeQuestion.objects.filter(exam=exam).order_by('pk')

    all_exam_questions_results = UserResults.objects.filter(exam_details=exam_details.id, username=username)

    total_points = 0
    exam_details.status = 'Evaluated'
    exam_details.result_status = 'Passed'
    for exam_question_result in all_exam_questions_results:
        if exam_question_result.status == 'Pending':
            exam_details.status = 'Pending'
            exam_details.result_status = 'Pending'
            exam_details.save()
        if exam_question_result.result == 'Incorrect':
            exam_details.result_status = 'Failed'
        total_points += exam_question_result.points

    start_time = exam_details.start_time
    end_time = exam_details.end_time
    time_elapsed = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
    exam_details.time_elapsed = time_elapsed
    exam_details.overall_points = total_points
    exam_details.save()
    return


def convertTimeString(hhmmss):
    if hhmmss != 'None':
        print(hhmmss)
        hms = hhmmss.split(':')
        for i in range(len(hms)):
            if len(hms[i]) == 1:
                hms[i] = '0' + str(hms[i])
        return f"{hms[0]}:{hms[1]}:{hms[2]}"


def generateFITB(question_text, answers):
    text = question_text
    count = 1
    for answer in answers:
        blank = f"<span><input type='text' id='fitb-{count}' name='answer-{count}' style='width: 10vw;'/></span>"
        text = text.replace(answer.answer, blank, 1)
        count += 1
    return text
