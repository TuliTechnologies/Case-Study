
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from . models import Users
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, args):
        data = super(TokenObtainPairSerializer, self).validate(args)
        refresh = self.get_token(self.user)

        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['middle_name'] = self.user.middle_name
        data['last_name'] = self.user.last_name
        data['type'] = self.user.type
        data['phone'] = self.user.phone
        data['gender'] = self.user.gender
        data['date_of_birth'] = self.user.date_of_birth
        data['id'] = self.user.id
        self.user.last_login = timezone.now()
        self.user.save()
        return data


class UsersSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'type', 'address', 'town', 'invoice_email')



# class CustomTokenSerializer(serializers.Serializer):
#     token = serializers.CharField()


class UpdateUserSerializer(ModelSerializer):
   

    class Meta:
        model = Users
        fields = ('id','first_name', 'last_name', 'phone', 'gender', 'date_of_birth', 'email', 'invoice_email', 'town', 'address')

    def update(self,request, validated_data):
        request.first_name = validated_data['first_name']
        request.last_name = validated_data['last_name']
        request.phone = validated_data['phone']
        request.gender = validated_data['gender']
        request.date_of_birth = validated_data['date_of_birth']
        request.email = validated_data['email']
        request.invoice_email = validated_data['invoice_email']
        request.town = validated_data['town']
        request.address = validated_data['address']
        
        request.save()

        return request


class ChangePasswordSerializer(serializers.Serializer):
    model = Users

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)        
