from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

urlpatterns = [
    # auth endpoints 
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),

    # user login
    path('front-user/login', views.FrontUserLoginTokenObtainPairView.as_view(), name='front_user_login'),
    path('admin/login', views.AdminLoginTokenObtainPairView.as_view(), name='admin_login'),
    path('supplier/login', views.SupplierLoginTokenObtainPairView.as_view(), name='supplier_login'),
    path('studio/login', views.StudioLoginTokenObtainPairView.as_view(), name='studio_login'),
    path('user/profile', views.UserProfileView.as_view(), name='user_profile'),

    # jwt endpoints 
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
