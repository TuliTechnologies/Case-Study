from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from . models import CustomerAddress, Order, OrderItem
from accounts.models import Users
from catalog_product.models import Products
from accounts.serializers import UsersSerializer
from supplier.serializers import SupplierSerializer
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from email.message import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
import smtplib
from rest_framework.views import APIView
import stripe
from rest_framework.decorators import api_view
from catalog_product.serializers import ProductSerializer
from catalog_product.models import SupplierProducts, ProductVariantBase, ProductVariants, ProductVariantSKU
from supplier.models import Supplier
from pages.models import Attributes, AttributeValues


# stripe.api_key = "sk_test_51I7Ex3H9mTaL1C9M743k2NE5sOJjthP1JZGNbSNwzHbzbiHMjOKWf7HK2n8rH9tEICAfOsLuFLS13rc7vLfh353J0034sr7Ofc"
# PUBLISHABLE_KEY = "pk_test_51I7Ex3H9mTaL1C9Mnqd1ljbQB87v4CdiGVf43hQVCU9NUZbb0Xshdq23grWdj4WguXLuNtl8FP8nEdYHrDckTYTB005Jpo6S96"


class CreateOrder(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Order.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):

        # order create
        order_detail = request.data['order']
        order_save = Order.objects.create(
            **order_detail)

        # order item

        order_item = request.data['orderItems']

        for item in order_item:
            item['order'] = order_save
        response_list = []
        for final_item in order_item:

            order_item_save = OrderItem.objects.create(
                **final_item)

            order_items_details = OrderItem.objects.filter(
                Q(is_deleted=False) and Q(pk=order_item_save.id)).values()
            response_list.append(order_items_details[0])

        currency_detail = request.data['Currency']

        currency_detail['order_id'] = order_save

        currency_save = Currency.objects.create(
            **currency_detail)
        # print("order_detail", order_detail['customer_id'])

        user_detail = Users.objects.get(
            Q(is_deleted=False) and Q(pk=order_detail['customer_id']))

        # SEND MAIL
        context = {
            'current_user': 'sss',

        }
        email_plaintext_message = render_to_string(
            'email/order_success.txt', context)
        email_html_message = render_to_string(
            'email/order_success.html', context)
        msg = EmailMultiAlternatives(
            # title:
            "Thanks For your Order at Digital Press",
            # message:
            email_plaintext_message,
            # from:
            "donotreply@digitalpress.co.uk",
            # to:
            [user_detail]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        # SEND STAGE MAIL
        context = {
            'current_user': 'sss',

        }
        email_plaintext_message = render_to_string(
            'email/stages/order_received.txt', context)
        email_html_message = render_to_string(
            'email/stages/order_received.html', context)
        msg = EmailMultiAlternatives(
            # title:
            "Thanks For your Order at Digital Press",
            # message:
            email_plaintext_message,
            # from:
            "donotreply@digitalpress.co.uk",
            # to:
            [user_detail]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        return Response({'status': 'success', 'message': "order created", 'order_items': response_list, 'order_id': order_save.id})


class UserOrder(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Order.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = OrderSerializer

    def list(self, request):

        queryset = Order.objects.filter(
            Q(is_deleted=False)).order_by('-updated_at').values()
        order_item = OrderItem.objects.filter(
            Q(is_deleted=False)).order_by('-updated_at').values()
        transection = Transaction.objects.filter(
            Q(is_deleted=False)).order_by('-updated_at').values()

        order_list = []
        order_items = []
        for data in queryset:
            for items in order_item:
                if items['order_id'] == data['id']:
                    order_items.append(items)
                    final_child = []
                    for sub in order_items:
                        if sub['order_id'] == data['id']:
                            final_child.append(sub)
                            data['items'] = final_child
        new = []
        for data in queryset:
            for tran in transection:
                if tran['id'] == data['transaction_id']:
                    new.append(tran)
                    data['transaction_id'] = new
        current_user = request.user
        user_detail = {'id': current_user.id,
                       'email': current_user.email, 'name': current_user.first_name}
        for data in queryset:
            if data["customer_id"] == user_detail["id"]:
                data["customer_id"] = user_detail
                order_list.append(data)

        return Response({'status': 'success', 'results': order_list})


class CustomerAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = CustomerAddress.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = CustomerAddressSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['customer'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):

        address = CustomerAddress.objects.filter(
            id=kwargs['pk'], is_deleted=False).first()
        data = request.data
        data['customer'] = request.user.id
        serializer = self.get_serializer(address, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):

        # order create
        order_detail = request.data['order']
        order_save = Order.objects.create(
            **order_detail)
        # order item

        order_item = request.data['orderItems']
        for item in order_item:

            order_item_data = {
                "order": order_save
            }
            order_item_save = OrderItem.objects.create(
                **order_item_data)
        # add currency
        currency_detail = request.data['Currency']
        currency_save = Currency.objects.create(
            **currency_detail)

        return Response({'order created'}, status=201)

# class CreateTransection(APIView):
#     def post(self,request, format=None):
#         user = request.user.id
#         tran_amount = request.data['tran_amount'] * 100
#         street1 = request.data['street1']
#         payment = stripe.Charge.create({'source':PUBLISHABLE_KEY,'tran_amount': tran_amount , 'tran_currency':'INR'})
#         final_transaction = Transaction(user_id = user, tran_amount= amount,street1=street1,batch_id =payment['id'] )
#         final_transaction.save()
#         return Response({'data': payment})


class QuotationView(viewsets.ModelViewSet):
    queryset = Quotation.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = QuotationSerializer


class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = OrderItemSerializer


class ShippingAddressView(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ShippingAddressSerializer

class BillingAddressView(viewsets.ModelViewSet):
    queryset = BillingAddress.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ShippingAddressSerializer


class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = TransactionSerializer


class UserArtworkView(viewsets.ModelViewSet):
    queryset = UserArtwork.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = UserArtworkSerializer


class GetOrderDetails(APIView):
    def get(self, request, order_id):
        print("ddd", order_id)
        queryset = Order.objects.filter(Q(is_deleted=False) and Q(
            pk=order_id)).order_by('-updated_at').values().first()

        order_items = OrderItem.objects.filter(
            Q(is_deleted=False) and Q(order=queryset['id'])).order_by('-updated_at').values()

        order_communication = OrderCommunication.objects.filter(
            Q(is_deleted=False) and Q(order_id=order_id)).order_by('-updated_at').values()
        # orderCommunicationSerializer = OrderCommunicationSerializer(order_communication).data
        queryset['order_communication'] = order_communication

        order_activity = OrderActivity.objects.filter(
            Q(is_deleted=False) and Q(order_id=order_id)).order_by('-updated_at').values()
        # orderCommunicationSerializer = OrderCommunicationSerializer(order_activity).data
        queryset['order_activity'] = order_activity

        for items in order_items:
            ## variant items
            product_variant = ProductVariants.objects.filter(
            Q(is_deleted=False) and Q(pk=items['catalog_product_variant_id'])).values().first()
            
            product_variant_sku = ProductVariantSKU.objects.filter(
            Q(is_deleted=False) and Q(product_variant=product_variant['id'])).values().first()

            items['variant'] = product_variant_sku


            product_variant_base = ProductVariantBase.objects.filter(
                Q(is_deleted=False) and Q(product_variant=product_variant['id'])).values()
            product_variant_sku['selected_variant'] = product_variant_base

            if product_variant_base is not None:
                for variant in product_variant_base:
                    
                    attribute = Attributes.objects.filter(
                    Q(is_deleted=False) and Q(pk=variant['attribute_id'])).values().first()
                    variant['attribute'] = attribute
                    
                    attribute_value = AttributeValues.objects.filter(
                    Q(is_deleted=False) and Q(pk=variant['attribute_value_id'])).values().first()
                    variant['attribute_value'] = attribute_value
                    
            product_data = Products.objects.filter(
                Q(is_deleted=False) and Q(pk=items['catalog_product_id'])).first()
            serializer = ProductSerializer(product_data).data
            items['product_data'] = serializer

            # :TODO - Need to Refactor this method
            product_supplier = SupplierProducts.objects.filter(
                Q(is_deleted=False) and Q(product_id=items['catalog_product_id'])).values()

            for data in product_supplier:

                supplier_list = Supplier.objects.filter(
                    Q(is_deleted=False) and Q(pk=data['supplier_id'])).values().first()

                data['supplier'] = supplier_list
            items['product_data']['product_supplier_list'] = product_supplier

            # assigned Supplier
            if items['supplier_id']:
                supplier_data = Supplier.objects.filter(
                    Q(is_deleted=False) and Q(pk=items['supplier_id'])).first()
                supplierSerializer = SupplierSerializer(supplier_data).data
                items['supplier'] = supplierSerializer

                print("YES COMES")

           # Artwork Proof
            artwork_proofing = ArtworkProofing.objects.filter(
                Q(is_deleted=False) and Q(order_item_id=items['id'])).order_by('-updated_at').values()
            # print("artwork_proofing", artwork_proofing)
            # serializer = ArtworkProofingSerializer(artwork_proofing).data
            items['artwork_proofing'] = artwork_proofing

            # add userArtworks
            user_artwork = UserArtwork.objects.filter(
                Q(is_deleted=False) and Q(order_item_id=items['id'])).first()
            userSerializer = UserArtworkSerializer(user_artwork).data
            items['user_artwork'] = userSerializer
            # print('user_artwork', user_artwork)

        user = Users.objects.filter(
            Q(is_deleted=False) and Q(pk=queryset['customer_id'])).values('id', 'first_name', 'last_name', 'email', 'phone').first()
        queryset['order_items'] = order_items
        queryset['user'] = user

        # print(order_items, "order_items")
        return Response({'status': 'success', 'results': queryset})


class SendProofingMail(APIView):
    def post(self, request, order_id):
        print('order_id', order_id)

        return Response({'status': 'Mail Sent'})


class DiscountCouponView(viewsets.ModelViewSet):
    queryset = DiscountCoupon.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = DiscountCouponSerializer


class OrderCommunicationView(viewsets.ModelViewSet):
    queryset = OrderCommunication.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = OrderCommunicationSerializer


class OrderActivityView(viewsets.ModelViewSet):
    queryset = OrderActivity.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = OrderActivitySerializer


class ArtworkProofingView(viewsets.ModelViewSet):
    queryset = ArtworkProofing.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ArtworkProofingSerializer

class SavedCardsView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = SavedCards.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = SavedCardsSerializer


class CheckDiscountCoupon(APIView):
    def get(self, request):
        queryset = DiscountCoupon.objects.filter(Q(is_deleted=False) and Q(
            coupon_code=request.data['coupon_code'])).values()
        if not queryset:
            return Response({'status': 'error', 'results': "Coupon Not Found"})

        return Response({'status': 'success', 'results': queryset[0]})

class GetDeliveryCost(APIView):
    def post(self, request):
        product_id = request.data['product_id']
        productData = []
        is_delivery_cost = False
        for id in product_id:
            print("iddd", id)
            product_data = Products.objects.filter(
                Q(is_deleted=False) and Q(pk=id)).values().first()
            print(product_data['is_delivery_applicable'])
            if(product_data['is_delivery_applicable'] == True):
                is_delivery_cost = True
            
            productData.append(product_data)
        
        print("is_delivery_cost", is_delivery_cost)
        base_price = 0
        if(is_delivery_cost == True):
            base_price = 14.95
            for calc in productData:
                if(calc['is_delivery_applicable'] == True):
                    if calc['prod_weight'] > 20:
                        cal_amount = calc['prod_weight'] - 20
                        base_price += cal_amount * 0.70
        else:
            base_price = 5.99

        return Response({'status': 'success', 'delivery_cost': base_price})
