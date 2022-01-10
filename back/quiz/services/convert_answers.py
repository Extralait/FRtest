from django.db import transaction
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from quiz.models import Quiz, Question, Answer


def convert_answers(quiz_pk, user, answers):
    quiz = Quiz.objects.prefetch_related(
        Prefetch(
            'question_set',
            queryset=Question.objects.all(),
            to_attr='questions'
        ),
        Prefetch(
            'questions__choice_set',
            to_attr='choices'
        ),
    ).get(pk=quiz_pk)

    checked_answers = []
    errors = {'errors': []}

    for question in quiz.questions:
        answer_dict = {'question_id': question.pk}
        is_empty = False
        answer_value = answers.get(str(question.pk))

        if question.question_type == 'text' and type(answer_value) == str:
            answer_dict['text_answer'] = answer_value

        elif question.question_type == 'checkbox' and type(answer_value) == list:
            choices_ids = list(map(lambda x: x.pk, question.choices))
            if all(map(lambda x: x in choices_ids, answer_value)):
                answer_dict['checkbox_answer'] = answer_value
            else:
                for choice in answer_value:
                    if choice not in choices_ids:
                        errors['errors'].append({
                            'detail': f'There is no option with id {choice} in the question {question.pk}'
                        })

        elif question.question_type == 'radio' and type(answer_value) == int:
            choices_ids = list(map(lambda x: x.pk, question.choices))
            if answer_value in choices_ids:
                answer_dict['radio_answer_id'] = answer_value
            else:
                errors['errors'].append({
                    'detail': f'There is no option with id {answer_value} in the question {question.pk}'
                })

        elif not question.is_required:
            is_empty = True

        else:
            errors['errors'].append({
                'detail': f'Not correct input type in question {question.pk}'
            })

        if not is_empty:
            checked_answers.append(answer_dict)

    if not len(errors['errors']):
        with transaction.atomic():
            for answer in checked_answers:
                question_id = answer.pop('question_id')
                checkbox_answer = answer.pop('checkbox_answer', None)

                result, created = Answer.objects.update_or_create(
                    user=user,
                    quiz_id=quiz_pk,
                    question_id=question_id,
                    defaults=answer
                )

                if checkbox_answer:
                    result.checkbox_answer.set(checkbox_answer)
                    result.save()

            user.passed_quiz.add(quiz)
            user.save()

        return Response(status=status.HTTP_200_OK)
    else:
        raise APIException(errors)
