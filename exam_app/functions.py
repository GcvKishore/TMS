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


def checkUserAnswers(exam_details_id):
    exam_details = UserExamDetails.objects.get(id=exam_details_id)

    username = exam_details.username
    exam = exam_details.exam
    questions = MakeQuestion.objects.filter(exam_model__id=exam.id).order_by('pk')

    for question in questions:
        user_question_details = UserQuestionDetails.objects.get(question=question.id, exam_details=exam_details)

        start_time = user_question_details.start_time
        end_time = user_question_details.end_time
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

    checkEvaluationStatus(exam_details_id)
    
    return


def checkEvaluationStatus(exam_details_id):
    exam_details = UserExamDetails.objects.get(id=exam_details_id)

    username = exam_details.username
    exam = exam_details.exam
    questions = MakeQuestion.objects.filter(exam_model__id=exam.id).order_by('pk')

    all_exam_questions_results = UserResults.objects.filter(exam_details=exam_details.id, username=username)

    total_points = 0

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
