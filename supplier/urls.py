from django.urls import path, include
from .import views
from rest_framework import routers
from .views import SupplierOrders, GetSupplierOrders

router = routers.DefaultRouter()
router.register(r'supplier', views.SupplierViewSet)
router.register(r'supplier-address', views.SupplierAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('supplier-order', SupplierOrders.as_view()),
    path('get-supplier-order/<int:order_id>/', GetSupplierOrders.as_view()),
]