from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *


class SupplierSerializer(ModelSerializer):

    class Meta:
        model = Supplier
        exclude = ('created_at','updated_at','is_deleted','deleted_at')

class SupplierAddressSerializer(ModelSerializer):

    class Meta:
        model = SupplierAddress
        exclude = ('created_at','updated_at','is_deleted','deleted_at')
