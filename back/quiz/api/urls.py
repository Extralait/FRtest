from django.conf.urls import url
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from quiz.api.views import QuizViewSet, QuestionViewSet, ChoiceViewSet

router = ExtendedSimpleRouter()

# Профиль пользователя
quiz_router = router.register(
    prefix=r'quiz',
    viewset=QuizViewSet,
    basename='quiz'
)
(
    # Уведомдения пользователя
    quiz_router.register(
        prefix=r'questions',
        viewset=QuestionViewSet,
        parents_query_lookups=['quiz'],
        basename='quiz-questions'
    ).register(
        prefix=r'choices',
        viewset=ChoiceViewSet,
        parents_query_lookups=['question__quiz', 'question'],
        basename='quiz-questions-choices'
    ),
)


urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
