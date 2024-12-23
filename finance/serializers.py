from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, BonusRequest

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'role', 'phone', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)

class BonusRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = ['id', 'title', 'reason', 'amount', 'status', 'created_by', 
                 'assigned_to', 'created_at', 'updated_at', 'attachment']
        read_only_fields = ['created_by', 'status']

# class AttachmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attachment
#         fields = '__all__'
