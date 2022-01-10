from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from quiz.models import Question, Choice, Quiz, Answer
from quiz.services.convert_answers import convert_answers


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Вариант (Сериализатор)
    """

    class Meta:
        model = Choice
        fields = ['id', 'title']


class AnswerSerializer(serializers.ModelSerializer):
    """
    Ответ (Сериализатор)
    """

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['user', 'quiz', 'question']

    def _user(self):
        """
        Получение текущего пользователя
        """
        return self.context['request'].user

    def update(self, instance, validated_data):
        """
        Обновить дроп
        """
        text_answer = validated_data.get('text_answer', None)
        checkbox_answer = validated_data.get('checkbox_answer', None)
        radio_answer = validated_data.get('radio_answer', None)
        if text_answer:
            answers = {str(instance.question.pk): text_answer}
        elif checkbox_answer:
            answers = {str(instance.question.pk): list(map(lambda x: x.pk, checkbox_answer))}
        elif radio_answer:
            answers = {str(instance.question.pk): radio_answer.pk}
        else:
            answers = {str(instance.question.pk): None}

        convert_answers(
            quiz_pk=str(instance.quiz.pk),
            user=self._user(),
            answers=answers
        )

        instance.text_answer = validated_data.get('text_answer', instance.text_answer)
        instance.radio_answer = validated_data.get('radio_answer', instance.radio_answer)
        try:
            instance.checkbox_answer.set(validated_data.get('checkbox_answer', instance.checkbox_answer))
        except TypeError:
            instance.groups.set(Choice.objects.none())

        return instance


class QuestionSerializer(WritableNestedModelSerializer):
    """
    Вопрос (Сериализатор)
    """
    choices = ChoiceSerializer(many=True, allow_null=True, required=False, source='choice_set')

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'is_required', 'choices']


class CreateQuizSerializer(WritableNestedModelSerializer):
    """
    Создать тест (Сериализатор)
    """
    questions = QuestionSerializer(many=True, allow_null=True, required=False, source='question_set')

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'is_active', 'start_date', 'end_date', 'questions']

    def _user(self):
        """
        Получение текущего пользователя
        """
        return self.context['request'].user

    def create(self, validated_data):
        """
        Создать дроп
        """

        validated_data['owner'] = self._user()
        return super().create(validated_data)


class QuizSerializer(WritableNestedModelSerializer):
    """
    Тест (Сериализатор)
    """
    questions = QuestionSerializer(many=True, allow_null=True, required=False, source='question_set')

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'owner', 'is_active', 'start_date', 'end_date', 'questions']
        read_only_fields = ['owner', 'start_date']


class AnswersSerializer(serializers.Serializer):
    """
    Ответ на тест (Сериализатор)
    """
    answers = serializers.JSONField()
