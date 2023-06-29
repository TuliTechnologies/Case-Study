from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *

# class BlogSerializer(ModelSerializer):

#     class Meta:
#         model = BlogData
#         exclude = ('is_deleted','deleted_at')

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('is_deleted','deleted_at')        
        depth = 1

class AttributeValueSerializer(ModelSerializer):

    class Meta:
        model = AttributeValues
        exclude = ('is_deleted','deleted_at')

class AttributeSerializer(ModelSerializer):
    attribute_values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attributes
        exclude = ('is_deleted','deleted_at')


class ProductTypeSerializer(ModelSerializer):

    class Meta:
        model = ProductTypes
        exclude = ('is_deleted','deleted_at')

class CategoryFAQSerializer(ModelSerializer):

    class Meta:
        model = CategoryFAQ
        exclude = ('is_deleted','deleted_at')

class ProductTypeAttributeValueSerializer(ModelSerializer):

    class Meta:
        model = ProductTypeAttributeValue
        exclude = ('is_deleted','deleted_at')
class ShippingTypeSerializer(ModelSerializer):

    class Meta:
        model = ShippingType
        exclude = ('is_deleted','deleted_at')
