from django.conf.urls import url
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from quiz.api.views import QuizViewSet, QuestionViewSet, ChoiceViewSet, AnswerViewSet
from users.api.views import UserViewSet

router = ExtendedSimpleRouter()

# Профиль пользователя
users_router = router.register(
    prefix=r'users',
    viewset=UserViewSet,
    basename='users'
)
(
    # Созданные тесты
    users_router.register(
        prefix=r'created-quiz',
        viewset=QuizViewSet,
        parents_query_lookups=['owner'],
        basename='user-created-quiz'
    ).register(
        prefix=r'questions',
        viewset=QuestionViewSet,
        parents_query_lookups=['quiz__owner','quiz'],
        basename='user-created-quiz-questions'
    ).register(
        prefix=r'choices',
        viewset=ChoiceViewSet,
        parents_query_lookups=['question__quiz__owner', 'question__quiz','question'],
        basename='user-created-quiz-questions-choices'
    ),
    # Пройденные тесты
    users_router.register(
        prefix=r'passed-quiz',
        viewset=QuizViewSet,
        parents_query_lookups=['interviewee'],
        basename='passed-quiz'
    ).register(
        prefix=r'answers',
        viewset=AnswerViewSet,
        parents_query_lookups=['quiz__interviewee', 'quiz'],
        basename='passed-quiz-answers'
    ),
)

urlpatterns = [
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # DRF router
    path('', include(router.urls)),
    # DRF GUI login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
