from rest_framework import serializers

from account.utils import Util
from .models import User
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'} , write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password2!=password:
            raise serializers.ValidationError("Password does not match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name',]

class UserPasswordChangeSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)

    class Meta:
        fields=['password','password2']

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password2!=password:
            raise serializers.ValidationError("Password does not match")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('ENCODED UID :',uid)
            token=PasswordResetTokenGenerator().make_token(user=user)
            print("Password reset token :",token)
            link="http://localhost:3000/api/user/reset/"+uid+"/"+token
            print("Password reset link : ",link)
            #send email
            body="Click on the link to reset the password"+link
            data={
                'subject':"Reset your password",
                'body':body,
                'to_email':user.email

            }
            Util.send_email(data=data)
            return attrs
        else:
            raise ValueError("This email is not registered")
        
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)

    class Meta:
        fields=['password','password2']

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        uid=self.context.get('uid')
        token=self.context.get('token')
        if password2!=password:
            raise serializers.ValidationError("Password does not match")
        id=smart_str(urlsafe_base64_decode(uid))
        user=User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user=user,token=token):
            raise ValueError("The token is not valid or expired")
        user.set_password(password)
        user.save()
        return attrs

        
