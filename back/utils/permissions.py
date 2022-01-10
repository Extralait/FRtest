from rest_framework.permissions import BasePermission

from quiz.models import Quiz, Question, Choice, Answer


class OwnerOrAdmin(BasePermission):
    """
    Владелец или администратор
    """

    def has_object_permission(self, request, view, obj):
        if type(obj) == Quiz:
            return obj.owner == request.user
        elif type(obj) == Question:
            return obj.quiz.owner == request.user
        elif type(obj) == Choice:
            return obj.question.quiz.owner == request.user
        elif type(obj) == Answer:
            return obj.user == request.user
        else:
            if request.user.is_staff:
                return True
            else:
                return False


class Nobody(BasePermission):
    """
    Никто не имеет доступ
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
