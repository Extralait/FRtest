from djoser.permissions import CurrentUserOrAdmin
from djoser.serializers import UserCreateSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from users.api.serializers import (
    UserDetailsSerializer,
    UserListSerializer,
)
from users.models import User
from utils.pagination import StandardResultsSetPagination


class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    filter_fields = [f.name for f in User._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def update_me(self, data):
        """
        Обновляет профиль текущего пользователя
        """
        user = self.request.user
        serializer = self.get_serializer(
            instance=user,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (CurrentUserOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора
        """
        if self.action == 'create':
            serializer_class = UserCreateSerializer
        elif self.action == 'list':
            serializer_class = UserListSerializer
        else:
            serializer_class = UserDetailsSerializer

        return serializer_class

    @action(
        detail=False,
        methods=['get'],
        name='me',
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, **kwargs):
        """
        Получить мой профиль
        """
        queryset = self.request.user
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request, **kwargs):
        return self.update_me(request.data)

    @me.mapping.put
    def put_me(self, request, **kwargs):
        return self.update_me(request.data)

    @me.mapping.delete
    def delete_me(self, request, **kwargs):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)

