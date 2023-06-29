from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import *
from django.db.models import Q
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from order_management.models import Order, OrderItem

class SupplierViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Supplier.objects.filter(Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = SupplierSerializer
class SupplierAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = SupplierAddress.objects.filter(Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = SupplierAddressSerializer

class SupplierOrders(APIView):
    def post(self, request):
        try:
            print("--", request.user.id)
            get_supplier = Supplier.objects.filter(
                Q(is_deleted=False) and Q(user=request.user.id)).order_by('-updated_at').values().first()

            print("get_supplier", get_supplier['id'])

        ### GET ITEMS BY Supplier ID ###
            queryset = OrderItem.objects.filter(
                Q(is_deleted=False) and Q(supplier=get_supplier['id'])).order_by('-updated_at').values()
            Order_List = []
            for item in queryset:
                ### GET Order Detail ###
                order_list = Order.objects.filter(
                    Q(is_deleted=False) and Q(pk=item['order_id'])).order_by('-updated_at').values().first()
                
                if order_list in Order_List:
                    print("EXISTS")
                else:
                    ### GET Order ITEMS ###
                    order_items = OrderItem.objects.filter(
                        Q(is_deleted=False) and Q(supplier=get_supplier['id']) and Q(order=order_list['id'])).order_by('-updated_at').values()
                    # print('----', order_items)
                    order_list['order_items'] = order_items
                    Order_List.append(order_list)

            return Response({'Order_list': Order_List})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)

class GetSupplierOrders(APIView):
    def post(self, request, order_id):
        try:
            get_supplier = Supplier.objects.filter(
                Q(is_deleted=False) and Q(user=request.user.id)).order_by('-updated_at').values().first()

            print("get_supplier", get_supplier['id'])
            order = Order.objects.filter(
                Q(is_deleted=False) and Q(pk=order_id)).order_by('-updated_at').values().first()
            
            order_items = OrderItem.objects.filter(
                    Q(is_deleted=False) and Q(supplier=get_supplier['id']) and Q(order=order_id)).order_by('-updated_at').values()
            order['order_items'] = order_items

            return Response({'Order_list': order})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)