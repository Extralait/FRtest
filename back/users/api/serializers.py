from django.contrib.auth.models import Permission, Group
from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """
    Лист пользователей (Сериализатор)
    """

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name'
        ]


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Детали текущего пользователя (сериализатор)
    """

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(UserDetailsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        read_only_fields = [
            'last_login', 'date_joined'
        ]
        exclude = ['password']

    def update(self, instance, validated_data):
        """
        Переопределение обновления пользователя
        """
        if instance.is_superuser or instance.is_staff:
            instance.is_active = validated_data.get('is_active', instance.is_active)

        if instance.is_superuser:
            instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
            instance.is_staff = validated_data.get('is_staff', instance.is_staff)
            try:
                instance.user_permissions.set(validated_data.get('user_permissions', instance.user_permissions))
            except TypeError:
                instance.user_permissions.set(Permission.objects.none())
            try:
                instance.groups.set(validated_data.get('groups', instance.groups))
            except TypeError:
                instance.groups.set(Group.objects.none())

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance
