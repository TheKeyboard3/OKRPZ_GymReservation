from rest_framework.serializers import ModelSerializer
from users.models import User


class UserListSerializer(ModelSerializer):
    """Список користувачів"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active')


class RecursiveSerializer(ModelSerializer):
    """Рекурсивний вивід childrens"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
