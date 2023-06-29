from rest_framework import viewsets, generics
from django.shortcuts import render
from . serializers import *
from . models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, UnsupportedMediaType, NotAcceptable
from rest_framework.parsers import FileUploadParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from pages.models import Attributes, AttributeValues
import pandas as pd
import numpy as np
from django.db.models import Q
import collections
import base64
from django.core.files.base import ContentFile
import json
from rest_framework import filters
import itertools
from variant.models import *



# class SoftDelete(viewsets.ModelViewSet):

#     def destroy(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.soft_delete()
#         return Response({
#             'status': 'success',
#             'message': 'Delete Success'
#         },
#             status=status.HTTP_200_OK
#         )

#     class Meta:
#         abstract = True


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Products.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active', 'is_premium', 'is_featured', 'is_trash']
    search_fields = ['name', 'description']

    # def create(self, request, format=None):
    #     if 'feature_image' in request.data:
    #         feature_image = request.data['feature_image']
    #         format, imgstr = feature_image.split(';base64,')
    #         ext = format.split('/')[-1]
    #         # You can save this as file instance.
    #         data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    #         request.data['feature_image'] = data
    #     # save to db
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductTrashViewSet(viewsets.ModelViewSet):

    queryset = Products.objects.filter(
        Q(is_deleted=False) and Q(is_trash=True)).order_by('-created_at')
    serializer_class = ProductSerializer

    # def create(self, request, format=None):
    #     if 'feature_image' in request.data:
    #         feature_image = request.data['feature_image']
    #         format, imgstr = feature_image.split(';base64,')
    #         ext = format.split('/')[-1]
    #         # You can save this as file instance.
    #         data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    #         request.data['feature_image'] = data
    #     # save to db
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImagesViewSet(viewsets.ModelViewSet):

    queryset = ProductImages.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ProductImagesSerializer


class ArtworksViewSet(viewsets.ModelViewSet):

    queryset = Artworks.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ArtworksSerializer

class FAQViewSet(viewsets.ModelViewSet):

    queryset = FAQ.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = FAQSerializer


class ProductDesignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ProductDesign.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ProductDesignSerializer


class ProductVariantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ProductVariants.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ProductVariantSerializer


class ShippingDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ShippingDetails.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ShippingDetailSerializer


class VariantsImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = VariantsImages.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = VariantsImageSerializer


class ProductPriceConfigrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ProductPriceConfigrations.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ProductPriceConfigrationSerializer


class SupplierProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = SupplierProducts.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = SupplierProductSerializer


class ProductVariantSet(APIView):
    def post(self, request, format=None):
        try:
            # create product variant
            product_id = request.data['product_id']
            # add product attributes
            for product_attribute in request.data['product_attribute']:
                product_attribute_data = {
                    'product_id':  product_id, 'attribute_id_id': product_attribute['attribute_id']}
                product_attribute_save = ProductAttribute.objects.create(
                    **product_attribute_data)

                for attribute_value in product_attribute['attribute_value_id']:
                    product_attribute_value_data = {
                        'product_attribute_id': product_attribute_save.id, 'attribute_value_id': attribute_value}

                    product_attribute_value_save = ProductAttributeValue.objects.create(
                        **product_attribute_value_data)

            for product_variant in request.data['catalog_product_variants']:

                # create product variant
                product_variant_data = {'product_id':  product_id}
                product_variant_store = ProductVariants.objects.create(
                    **product_variant_data)

                for product_variant_base in product_variant['attributes']:
                    # this for loop is for attribute_value data
                    for attribute_value in product_variant_base['attribute_value_id']:
                        product_variant_base_data = {'product_id':  product_id, 'product_variant_id': product_variant_store.id, 'base_attribute_id': request.data[
                            'base_attribute_id'], 'attribute_id': product_variant_base['attribute_id'], 'attribute_value_id': attribute_value}

                        # create product variant base
                        product_variant_base_save = ProductVariantBase.objects.create(
                            **product_variant_base_data)

                # create product SKU and price
                product_variant_detail = product_variant['details']

                for priceConfig in product_variant_detail['prices']:
                    product_variant_sku_data = {'product_id':  product_id, 'product_variant_id': product_variant_store.id, 'express_price': priceConfig[
                        'express_price'], 'value_price': priceConfig['value_price'], 'standard_price': priceConfig['standard_price'], 'quantity': priceConfig['quantity'], 'sku': priceConfig['sku']}
                    product_variant_sku_save = ProductVariantSKU.objects.create(
                        **product_variant_sku_data)

            return Response({'Status': 'Success', 'data': request.data})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)



class GetProductVariant(APIView):
    def get(self, request, product_id):

        product_variant = ProductVariants.objects.filter(product=product_id).values()
        for variant in product_variant:
            
            product_variant_base = ProductVariantBase.objects.filter(product_variant=variant['id']).values()

            grouped_data = []
            for attribute_id, group in itertools.groupby(product_variant_base, key=lambda x: x['attribute_id']):
                attribute_values = [obj['attribute_value_id'] for obj in group]
                grouped_data.append({'attribute_id': attribute_id, 'attribute_values': attribute_values})

            for group in grouped_data:
                print('group', group) 
                attribute = Attributes.objects.filter(pk=group['attribute_id']).values().first()
                group['attribute'] = attribute
                
                attribute_value = AttributeValues.objects.filter(pk=group['attribute_values'][0]).values().first()
                group['attribute_value'] = attribute_value

            variant['variant'] = grouped_data
            
            product_variant_sku = ProductVariantSKU.objects.filter(product_variant=variant['id']).values()
            variant['details'] = product_variant_sku

        return Response({'status': 'success', 'data': { 'catalog_product_variants': product_variant, 'product_attribute': grouped_data, 'product_id': product_id}})


class UpdateProductVariant(APIView):
    def post(self, request, product_id):
        return Response({'status': 'success'})

class GetCatalogProduct(APIView):
    def get(self, request, product_id):
        # get Product data
        product = Products.objects.filter(
            Q(is_deleted=False) and Q(pk=product_id)).first()
        serializer = ProductSerializer(product).data

        associates = VariantAssociatedAttributes.objects.filter(
            Q(is_deleted=False) and Q(product_id=product.id)).values()
        
        
        # new query # associated_attribute
        combined_data = {}
        for obj in associates:
            attribute_id = obj["attribute_id"]
            attribute_value_id = obj["attribute_value_id"]
            
            if attribute_id not in combined_data:
                combined_data[attribute_id] = {"attribute_id": attribute_id, "attribute_value": [attribute_value_id]}
            else:
                combined_data[attribute_id]["attribute_value"].append(attribute_value_id)

        output = list(combined_data.values())
        associate_data = []
        for acc in output:
            
            attribute = Attributes.objects.filter(
                Q(is_deleted=False) and Q(pk=acc['attribute_id'])).values().first()
            attribute['attribute_name'] = attribute['name']
            attribute['attribute_is'] = attribute['id']
            attribute_values = []
            for attribute_value in acc['attribute_value']:
                attribute_value = AttributeValues.objects.filter(
                    Q(is_deleted=False) and Q(pk=attribute_value)).values().first()
                attribute_value['value_name'] = attribute_value['name']
                attribute_value['value_id'] = attribute_value['id']

                attribute_values.append(attribute_value)
            attribute['attribute_value']= attribute_values

            associate_data.append(attribute)
            
        # NEW PRICEING LOGIC
        product_variant = ProductVariant.objects.filter(
            Q(is_deleted=False) and Q(product=product)).values().first()
        serializer['variant'] = {}

        if product_variant is not None:

            product_variant_sku = ProductVariantPrice.objects.filter(
                Q(is_deleted=False) and Q(product_variant=product_variant['id'])).values()

            product_variant['pricing'] = product_variant_sku
            serializer['variant'] = product_variant


        ## THIS IS FOR ARTWORK ##
        artworks = Artworks.objects.filter(
            Q(is_deleted=False) and Q(product_id=product)).values()
        if artworks is not None:
            serializer['artworks'] = artworks


        serializer['associated_attribute'] = associate_data
        return Response(serializer)


class FilterPricing(APIView):
    def post(self, request):
        try:
            attribute_value_id = request.data['attribute_value_id']
            product_id = request.data['product_id']

            # get Product data
            product_variant_data = ProductVariant.objects.filter(
                Q(is_deleted=False) and Q(product=product_id)).values()

            listDist = []
            for index, value in enumerate(product_variant_data):
                product_variant_base = ProductVariantCombination.objects.filter(
                    Q(is_deleted=False) and Q(product=product_id) and Q(product_variant=value['id'])).values()

                setValue = []
                for checkAttribute in attribute_value_id:
                    queryset = bool(product_variant_base.filter(
                        attribute_value=checkAttribute))
                    setValue.append(queryset)
                    listDist.append(value['id'])

                if False in setValue:
                    continue
                ID = product_variant_base[0]['product_variant_id']
                ProductPricing = ProductVariantPrice.objects.filter(
                    Q(is_deleted=False) and Q(product_variant=ID)).values()

            return Response({'pricing': ProductPricing})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)



class DesignServiceViewSet(viewsets.ModelViewSet):

    queryset = DesignService.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = DesignServiceSerializer

class DeliverySettingsViewSet(viewsets.ModelViewSet):

    queryset = DeliverySettings.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = DeliverySettingsSerializer

class DeliveryMethodsViewSet(viewsets.ModelViewSet):

    queryset = DeliveryMethods.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = DeliveryMethodsSerializer
