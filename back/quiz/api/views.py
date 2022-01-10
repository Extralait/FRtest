from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from quiz.api.serializers import CreateQuizSerializer, AnswersSerializer, AnswerSerializer, QuestionSerializer, \
    ChoiceSerializer
from quiz.api.serializers import QuizSerializer
from quiz.models import Quiz, Choice, Question, Answer
from quiz.services.convert_answers import convert_answers
from utils.pagination import StandardResultsSetPagination
from utils.permissions import OwnerOrAdmin, Nobody


class QuizViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Тест (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Quiz.objects.all()
    filter_fields = [f.name for f in Quiz._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve', 'answer']:
            permission_classes = (AllowAny,)
        elif self.action in ['create']:
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (OwnerOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора
        """
        if self.action == 'create':
            serializer_class = CreateQuizSerializer
        elif self.action == 'answer':
            serializer_class = AnswersSerializer
        else:
            serializer_class = QuizSerializer

        return serializer_class

    @action(
        detail=True,
        methods=['post'],
        name='answer',
        url_path='answer',
        permission_classes=(AllowAny,),
    )
    def answer(self, request, **kwargs):
        """
        Ответить на тест
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            answers = serializer.validated_data['answers']

            if self.request.user.is_anonymous:
                user = None
            else:
                user = self.request.user
            return convert_answers(
                quiz_pk=int(self.kwargs.get('pk')),
                user=user,
                answers=answers
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ChoiceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Вариант (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_fields = [f.name for f in Choice._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action == ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (OwnerOrAdmin,)

        return [permission() for permission in permission_classes]


class QuestionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Вопрос (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_fields = [f.name for f in Question._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action == ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (OwnerOrAdmin,)

        return [permission() for permission in permission_classes]


class AnswerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Вариант (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_fields = [f.name for f in Answer._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action == ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (OwnerOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Answer.objects.all()
        elif type(self.request.user) == AnonymousUser:
            queryset = Answer.objects.none()
        else:
            queryset = Answer.objects.filter(user=user).all()
        return self.filter_queryset_by_parents_lookups(
            queryset
        )
