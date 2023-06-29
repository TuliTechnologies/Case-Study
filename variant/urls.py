from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register(r'supplier', views.SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-variant/', CreateVariant.as_view()),
    path('update-variant/', UpdateVariant.as_view()),
    path('get-variant/', GetVariant.as_view()),
    path('get-variant-by-id/<int:variant_id>', GetVariantByID.as_view()),
]