from users.api.urls import urlpatterns as users
from quiz.api.urls import urlpatterns as quiz

urlpatterns = []
urlpatterns += users
urlpatterns += quiz
