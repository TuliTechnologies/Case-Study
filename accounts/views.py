from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from . models import Users
from . serializers import UserTokenObtainPairSerializer, UsersSerializer, UpdateUserSerializer, ChangePasswordSerializer
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from email.message import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
import smtplib
from rest_framework import generics

from rest_framework import status


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
  
  try:
    
    if 'first_name' not in request.data and request.data['type']  == 'front_user':
      return Response({'status':'error', 'message': 'first_name required.'}, status=404)

    
    password = request.data.get('password')

    serializer = UsersSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    data['is_active'] = True

    if not password:
        return Response({'status':'error','message': 'user password is required'}, status=404)

    if Users.objects.filter(email=data.get('email')).exists():
        return Response({'status':'error','message': 'Email is taken'}, status=400)
    else:
        user = Users(**data)
        user.set_password(password)
        user.save()
        if 'first_name' in request.data and request.data['type']  == 'front_user':
            email_plaintext_message = render_to_string('email/welcome_email.txt')
            email_html_message = render_to_string('email/welcome_email.html')
            msg = EmailMultiAlternatives(
                    # title:
                    "Welcome To Digital Press",
                    # message:
                    email_plaintext_message,
                    # from:
                    "donotreply@digitalpress.co.uk",
                    # to:
                    [request.data['email']]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()
    user_id = Users.objects.filter(email=user).values()
    print("user_id", user_id[0]['id'])
    return Response({'status':'success', 'message': 'Successfully signed up please login.', 'user_id': user_id[0]['id']}, status=201)
  
  except ValidationError as e: 
    return Response({'status':'error', 'message': e.detail}, status=404)
  except Exception as e: 
    return Response({'status':'error', 'message': str(e)}, status=404)


class UserProfileView(APIView):

  permission_classes = (IsAuthenticated,)

  def get(self, request, *args, **kwargs):

    return Response(UsersSerializer(request.user).data, status=200)

  def patch(self, request, *args, **kwargs):
    user = request.user

    serializer = UsersSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(serializer.errors, status=400)

    return Response(serializer.data, status=201)


class FrontUserLoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='front_user').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            
        return Response(serializer.validated_data, status=200)

class AdminLoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='admin').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            
        return Response(serializer.validated_data, status=200)

class SupplierLoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='supplier').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            
        return Response(serializer.validated_data, status=200)

class StudioLoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='studio').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            
        return Response(serializer.validated_data, status=200)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return Response({'status':'success','message': 'Logout Success'}, status=200)
  else:
    return Response({'status':'error','message': 'Method Not Allowed'}, status=405)

        
class UpdateProfileView(generics.UpdateAPIView):

    queryset = Users.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = Users
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


