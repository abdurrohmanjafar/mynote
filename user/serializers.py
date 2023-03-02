from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        read_only_fields = ('id',)
        fields = '__all__'

    def save(self):
        user = CustomUser(
            email=self.validated_data['email'],
        )

        password = self.validated_data['password']
        user.set_password(password)

        user.save()
        return user