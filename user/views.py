from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import *
from django.db.models import Q
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from order_management.models import Order, OrderItem, ShippingAddress, BillingAddress, SavedCards

# Create your views here.
class SupplierOrders(APIView):
    def post(self, request):
        try:
            order_list = Order.objects.filter(
                Q(is_deleted=False) and Q(customer=request.user.id)).order_by('-updated_at').values()
            
            for order in order_list:
                order_item_list = OrderItem.objects.filter(
                    Q(is_deleted=False) and Q(order=order['id'])).order_by('-updated_at').values()
                order['order_items'] = order_item_list

            # print("order_list", order_list)
            
            return Response({'message': 'success', 'result': order_list})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)


class UserBillingAddress(APIView):
    def post(self, request):
        try:
            billing_address = BillingAddress.objects.filter(
                Q(is_deleted=False) and Q(customer=request.user.id)).order_by('-updated_at').values()
           
            return Response({'message': 'success', 'result': billing_address})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)


class UserShippingAddress(APIView):
    def post(self, request):
        try:
            shipping_address = ShippingAddress.objects.filter(
                Q(is_deleted=False) and Q(customer=request.user.id)).order_by('-updated_at').values()
           
            
            return Response({'message': 'success', 'result': shipping_address})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)

class UserSavedCards(APIView):
    def post(self, request):
        try:
            saved_cards = SavedCards.objects.filter(
                Q(is_deleted=False) and Q(user=request.user.id)).order_by('-updated_at').values()
           
            
            return Response({'message': 'success', 'result': saved_cards})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)
