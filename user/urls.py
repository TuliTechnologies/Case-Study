from django.urls import path, include
from .import views
from rest_framework import routers
from .views import SupplierOrders, UserBillingAddress, UserShippingAddress, UserSavedCards

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('user-order', SupplierOrders.as_view()),
    path('user-billing-address', UserBillingAddress.as_view()),
    path('user-shipping-address', UserShippingAddress.as_view()),
    path('user-saved-cards', UserSavedCards.as_view()),
]