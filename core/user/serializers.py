from rest_framework import serializers
from datetime import date
from .models import MyUser, Refer

from random import choices
from string import ascii_uppercase, digits

from .utils import check_email_existence

import requests


class UserCreateSerializer(serializers.ModelSerializer):
    
    referal_code = serializers.CharField(required = False, allow_blank = True, write_only = True)
    
    class Meta:
        model = MyUser
        fields = (
            'email', 
            'username',
            'password',
            'referal_code'
        )
    
    def validate(self, attrs):
        email = attrs['email']
        
        is_email = check_email_existence(email) # checking email existance with emailhunter API
        
        if not is_email:
            raise serializers.ValidationError({"email": "doesn't exist"})

        # Logic for referal_code
        if 'referal_code' in attrs:
            ref_code = attrs['referal_code']
            if ref_code != '':
                ref_instance = Refer.objects.filter(code=ref_code, expire_date__gt=date.today()).first()

                if ref_instance is not None:
                    attrs['referal'] = ref_instance
                else:
                    raise serializers.ValidationError({"referal_code": "not found!"})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        ref_instance = None
        if 'referal_code' in validated_data:
            validated_data.pop('referal_code')
        
        if 'referal' in validated_data:
            ref_instance = validated_data.pop('referal')
            
        user = MyUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        if ref_instance is not None:
            ref_instance.user.score += 50
            ref_instance.user.save()
            user.score += 40
            user.save()
            ref_instance.users.add(user)
            ref_instance.save()
        
        return user
    
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field == 'password':
                instance.set_password(value)
            else:
                setattr(instance, field, value)
        instance.save()
        return instance

class ReferCreateSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    code = serializers.CharField(read_only = True)
    
    class Meta:
        model = Refer
        fields = ('code', 'user', 'expire_date')
    
    def create(self, validated_data):
        
        code = ''.join(choices(ascii_uppercase + digits, k = 10))

        # Code generation logic
        while True:
            code = ''.join(choices(ascii_uppercase + digits, k = 10)) 
            ref_instance = Refer.objects.filter(code=code).first()
            if ref_instance is None:
                break
            
        validated_data['code'] = code
        
        return Refer.objects.create(**validated_data)
    
class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')

class UserDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'created_date')

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(default = 'It is test message')
    message = serializers.CharField(read_only = True)
    receiver = serializers.EmailField()
    pk = serializers.IntegerField(read_only = True)
    
        
