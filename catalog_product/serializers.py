from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from pages.serializers import AttributeSerializer, AttributeValueSerializer, ProductTypeSerializer, ProductTypeAttributeValueSerializer
from pages.models import Attributes
from .models import *


class ProductPriceConfigrationSerializer(ModelSerializer):

    class Meta:
        model = ProductPriceConfigrations
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ProductImagesSerializer(ModelSerializer):

    class Meta:
        model = ProductImages
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ArtworksSerializer(ModelSerializer):

    class Meta:
        model = Artworks
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class FAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ProductDesignSerializer(ModelSerializer):

    class Meta:
        model = ProductDesign
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ProductVariantBaseSerializer(ModelSerializer):

    class Meta:
        model = ProductVariantBase
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ProductVariantSKUSerializer(ModelSerializer):
    
    
    class Meta:
        model = ProductVariantSKU
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ProductVariantSerializer(ModelSerializer):
    product_variant_base = ProductVariantBaseSerializer(many=True, read_only=True)
    product_attribute  = AttributeSerializer(many=True, read_only=True)
    product_variant_sku = ProductVariantSKUSerializer(many=True, read_only=True)
    class Meta:
        model = ProductVariants
        exclude = ('created_at','updated_at','is_deleted','deleted_at')


class ShippingDetailSerializer(ModelSerializer):

    class Meta:
        model = ShippingDetails
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
        
class VariantsImageSerializer(ModelSerializer):

    class Meta:
        model = VariantsImages
        exclude = ('created_at','updated_at','is_deleted','deleted_at')


class DesignServiceSerializer(ModelSerializer):
    class Meta:
        model = DesignService
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class DeliverySettingsSerializer(ModelSerializer):
    class Meta:
        model = DeliverySettings
        exclude = ('created_at','updated_at','is_deleted','deleted_at')


class DeliveryMethodsSerializer(ModelSerializer):

    class Meta:
        model = DeliveryMethods
        exclude = ('created_at','updated_at','is_deleted','deleted_at')


class SupplierProductSerializer(ModelSerializer):

    class Meta:
        model = SupplierProducts
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
        # depth = 1
        
        def __init__(self, *args, **kwargs):
            super(SupplierProductSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')

            if request and request.method=='POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1

        
class ProductSerializer(ModelSerializer):
    artworks = ArtworksSerializer(many=True, read_only=True)
    faq = FAQSerializer(many=True, read_only=True)
    product_design = ProductDesignSerializer(many=True, read_only=True)
    shipping_details = ShippingDetailSerializer(many=True, read_only=True)
    attributes_variants = ProductTypeSerializer(many=True, read_only=True)
    product_images = ProductImagesSerializer(many=True,     read_only=True)
    product_design_service = DesignServiceSerializer(many=True,     read_only=True)
    product_delivery_settings = DeliverySettingsSerializer(many=True,     read_only=True)
    product_delivery_methods = DeliveryMethodsSerializer(many=True,     read_only=True)
    product_supplier = SupplierProductSerializer(many=True,     read_only=True)
    class Meta:
        model = Products
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
        # depth = 1

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method=='POST':
            self.Meta.depth = 0
        elif request and request.method=='PATCH':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1



class AttributeSerializer(ModelSerializer):

    class Meta:
        model = Attributes
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class ProductAttributeSerializer(ModelSerializer):    
    author_name = serializers.ReadOnlyField(source="Attributes.name")

    class Meta:
        model = ProductAttribute
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
