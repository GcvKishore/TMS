from .models import *


def validate_answers(user_answers, correct_answers):
    if len(user_answers) != len(correct_answers):
        return 'Incorrect'

    user_inputs = []
    for answer in user_answers:
        user_inputs.append(answer.answer_text_input.lower())

    answers = []
    for correct_answer in correct_answers:
        answers.append(correct_answer.answer.lower())

    for user_answer in user_inputs:
        if user_answer not in answers:
            return 'Incorrect'

    return 'Correct'


def checkUserAnswers(exam_details_id):
    exam_details = UserExamDetails.objects.get(id=exam_details_id)
    print("passed")

    username = exam_details.username
    exam = exam_details.exam
    questions = MakeQuestion.objects.filter(exam_model__id=exam.id).order_by('pk')
    print(len(questions))

    for question in questions:
        user_question_details = UserQuestionDetails.objects.get(question=question.id, exam_details=exam_details)
        if not question.evaluation_type or None:
            UserResults.objects.filter(username=username, exam_details=exam_details,
                                       question=question).delete()
            UserResults.objects.create(
                username=username,
                exam_details=exam_details,
                question_type=question.question_type,
                question=question,
                status='Pending',
                result='Pending',
                points=0,
                time_elapsed=user_question_details.time_elapsed
            ).save()
            return

        user_answers = UserAnswerTextInput.objects.filter(question=user_question_details.id)
        correct_answers = Answer.objects.filter(question=question.id)

        result = validate_answers(user_answers, correct_answers)

        UserResults.objects.filter(username=username, exam_details=exam_details,
                                   question=question).delete()
        UserResults.objects.create(
            username=username,
            exam_details=exam_details,
            question_type=question.question_type,
            question=question,
            status='Evaluated',
            result=result,
            points=None,
            time_elapsed=user_question_details.time_elapsed
        ).save()

    all_exam_questions_results = UserResults.objects.filter(exam_details=exam_details.id, username=username)

    for exam_question_result in all_exam_questions_results:
        if exam_question_result.status == 'Pending':
            exam_details.status = 'Pending'
            exam_details.result_status = 'Pending'
            exam_details.save()
            return
        if exam_question_result.result == 'Incorrect':
            exam_details.result_status = 'Failed'
            exam_details.save()
    return None
