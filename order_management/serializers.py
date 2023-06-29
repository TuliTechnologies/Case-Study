from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . models import *
# from accounts.serializers import UsersSerializer
from accounts.models import Users


class CustomerAddressSerializer(ModelSerializer):

    class Meta:
        model = CustomerAddress
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class CreditCardSerializer(ModelSerializer):

    class Meta:
        model = CreditCard
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class ShippingMethodSerializer(ModelSerializer):

    class Meta:
        model = ShippingMethod
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class ShippingAddressSerializer(ModelSerializer):

    class Meta:
        model = ShippingAddress
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class DiscountSetSerializer(ModelSerializer):

    class Meta:
        model = DiscountSet
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class DiscountSerializer(ModelSerializer):

    class Meta:
        model = Discount
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class DiscountAssociationSerializer(ModelSerializer):

    class Meta:
        model = DiscountAssociation
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class TransactionEntrySerializer(ModelSerializer):

    class Meta:
        model = TransactionEntry
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class UserArtworkSerializer(ModelSerializer):

    class Meta:
        model = UserArtwork
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ArtworkProofingSerializer(ModelSerializer):

    class Meta:
        model = ArtworkProofing
        exclude = ('deleted_at',)

class OrderItemSerializer(ModelSerializer):
    
    user_artwork = UserArtworkSerializer(many=True, read_only=True)
    artwork_proofing_item = ArtworkProofingSerializer(many=True, read_only=True)

    # def __init__(self, *args, **kwargs):
    #     print("COMES HERE")
    #     super(OrderItemSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    
    #     print("request", request)
    #     if request and request.method=='POST':
    #         print("request", request.method)
    #         self.Meta.depth = 0
    #     elif request and request.method=='PATCH':
    #         print("PATCH", request.method)
    #         self.Meta.depth = 0
    #     else:
    #         print("34", request.method)
            
    #         self.Meta.depth = 1
    class Meta:
        model = OrderItem
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
        # depth = 1

        def __init__(self, *args, **kwargs):
            print("COMES HERE")
            super(OrderItemSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')

            if request and request.method=='POST':
                self.Meta.depth = 0
            elif request and request.method=='PATCH':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1


class UsersSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'type')


class OrderCommunicationSerializer(ModelSerializer):

    class Meta:
        model = OrderCommunication
        exclude = ('created_at','updated_at','is_deleted','deleted_at')


class OrderActivitySerializer(ModelSerializer):

    class Meta:
        model = OrderActivity
        exclude = ('deleted_at',)


class OrderSerializer(ModelSerializer):
    
    order_communication = OrderCommunicationSerializer(many=True, read_only=True)
    artwork_proofing = ArtworkProofingSerializer(many=True, read_only=True)
    order_activity = OrderActivitySerializer(many=True, read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='customer')

    class Meta:
        model = Order
        exclude = ('is_deleted','deleted_at')
        depth = 1

class OrderAdjustmentSerializer(ModelSerializer):

    class Meta:
        model = OrderAdjustment
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class OrderLineAdjustmentSerializer(ModelSerializer):

    class Meta:
        model = OrderLineAdjustment
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class OrderLineSerializer(ModelSerializer):

    class Meta:
        model = OrderLine
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class CurrencySerializer(ModelSerializer):

    class Meta:
        model = Currency
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class SavedItemSerializer(ModelSerializer):

    class Meta:
        model = SavedItem
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class SecuritySerializer(ModelSerializer):

    class Meta:
        model = Security
        exclude = ('created_at','updated_at','is_deleted','deleted_at')



class QuotationSerializer(ModelSerializer):

    class Meta:
        model = Quotation
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
class ShippingAddressSerializer(ModelSerializer):

    class Meta:
        model = ShippingAddress
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class BillingAddressSerializer(ModelSerializer):

    class Meta:
        model = BillingAddress
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class DiscountCouponSerializer(ModelSerializer):

    class Meta:
        model = DiscountCoupon
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
        

class SavedCardsSerializer(ModelSerializer):

    class Meta:
        model = SavedCards
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
        
