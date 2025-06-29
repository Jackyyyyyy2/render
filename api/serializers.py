from rest_framework import serializers
from pos_app.models import (User,TujuanDinas,StatusModel,KategoriBiaya,PengajuanDinas)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all())
    ])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_active', 'is_pegawai', 'is_atasan', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Kata sandi dan ulangi sandi tidak sama.'})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            is_pegawai=validated_data['is_pegawai'],
            is_atasan=validated_data['is_atasan'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError({'message': 'Status pengguna tidak aktif...'})
            else:
                raise ValidationError({'message': 'Anda tidak memiliki akses masuk...'})
        else:
            raise ValidationError({'message': 'Mohon mengisi kolom nama pengguna dan kata sandi...'})
        return data
    
class TujuanDinasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TujuanDinas
        fields = '__all__'

class StatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = '__all__'

class KategoriBiayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KategoriBiaya
        fields = '__all__'

class PengajuanDinasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PengajuanDinas
        fields = '__all__'

