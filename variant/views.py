from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProductVariant, ProductVariantCombination, ProductVariantPrice, VariantAssociatedAttributes
from pages.models import Attributes, AttributeValues
from django.db.models import Q

class CreateVariant(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')

        # // associated_attribute
        associated_attribute = request.data.get('associated_attribute')
        varints = request.data.get('variants')
    
        # // THIS WILL BE FOR DELETE/SOFT DELETE
        delete_variant = VariantAssociatedAttributes.objects.filter(product_id=product_id)
        for delete in delete_variant:
            delete.delete()
        print("BEFORE DELETE")

        ProductVariant.objects.filter(product_id=product_id).delete()

        ProductVariantCombination.objects.filter(product_id=product_id).delete()
          # // delete Method
        ProductVariantPrice.objects.filter(product_id=product_id).delete()


        print("AFTER DELETE")
        for attribute in associated_attribute:

            for attribute_value in attribute['attribute_value_id']:
                    dict_data = {'attribute_value_id': attribute_value, 'attribute_id':
                                 attribute['attribute_id'], 'product_id': product_id}
                    product_obj = VariantAssociatedAttributes.objects.create(
                        **dict_data)
                    product_obj.save()

        for varint in varints:
            # // add product variant
            product_variant_data = {'product_id':  product_id}
            product_variant_store = ProductVariant.objects.create(
                **product_variant_data)



            # // Add product variant combinations
            for product_variant in varint['option_values']:
                # // set combination
                product_variant_combination_data = {
                    'product_id':  product_id, 'product_variant_id': product_variant_store.id, 'attribute_id': product_variant['option_id'], 'attribute_value_id': product_variant['value_id']}


                # // add product variant combination
                ProductVariantCombination.objects.create(
                    **product_variant_combination_data)

            

            for variant_price in varint['prices']:
                # // set combination
                product_variant_price_data = {
                    'product_id':  product_id, 'product_variant_id': product_variant_store.id, 'express_price': variant_price['express'], 'standard_price': variant_price['standard'], 'value_price': variant_price['value'], 'quantity': variant_price['quantity'], }


                # // add product variant combination
                ProductVariantPrice.objects.create(
                    **product_variant_price_data)

        return Response({'Status': product_variant_price_data})



class GetVariantByID(APIView):
    def get(self, request, variant_id):

        product_variant_combination = ProductVariantCombination.objects.filter(
            product_variant=variant_id).values()


        for variant in product_variant_combination:

            attribute = Attributes.objects.filter(
                pk=variant['attribute_id']).values().first()
            variant['attribute'] = attribute

            print(attribute, "attribute")
            attribute_value = AttributeValues.objects.filter(
                pk=variant['attribute_value_id']).values().first()
            variant['attribute_value'] = attribute_value
            
        
        return Response({'Status': product_variant_combination})


class GetVariant(APIView):
    def post(self, request):
        response = {}

        response_data = {}
        product_id = request.data.get('product_id')

        # // Get associated attribute

        product_type_attribute_value = VariantAssociatedAttributes.objects.filter(
            Q(is_deleted=False) and Q(product_id=product_id)).values()
        for data in product_type_attribute_value:
            attribute_values = AttributeValues.objects.filter(
                Q(is_deleted=False) and Q(pk=data['attribute_value_id'])).values()
            all_attribute_values = AttributeValues.objects.filter(
                Q(is_deleted=False) and Q(attribute=data['attribute_id'])).values()
            attribute = Attributes.objects.filter(
                Q(is_deleted=False) and Q(pk=data['attribute_id'])).values()

            data['attribute_value'] = attribute_values[0]
            data['all_attribute_values'] = all_attribute_values
            data['attribute'] = attribute[0]
            data['product_type_attribute_value'] = data['id']

        response_data['product_type_values'] = product_type_attribute_value

        print(response_data, "response_data")

        # // Get variant
        product_variant = ProductVariant.objects.filter(
            product_id=product_id).values()

        for variant in product_variant:

            # // get Combination
            product_variant_combination = ProductVariantCombination.objects.filter(
                product_variant=variant['id']).values()

            combination_array = []
            for combination in product_variant_combination:
                attribute = Attributes.objects.filter(
                    pk=combination['attribute_id']).values().first()
                attribute_value = AttributeValues.objects.filter(
                    pk=combination['attribute_value_id']).values().first()
                option_dict = {'option_id': combination['attribute_id'], 'option': attribute,
                               'value_id': combination['attribute_value_id'], 'value': attribute_value}
                combination_array.append(option_dict)

            variant['option_values'] = combination_array

            # // get Prices
            price_array = []
            product_price_combination = ProductVariantPrice.objects.filter(
                product_variant=variant['id']).values()
            for prices in product_price_combination:
                price_dict = {'express': prices['express_price'],'standard': prices['standard_price'],'value': prices['value_price'],'quantity': prices['quantity'], }
                price_array.append(price_dict)
            variant['prices'] = price_array

        response['variants'] = product_variant
        response['associated_attribute'] = response_data
        response['product_id'] = product_id
        return Response({'Status': 'success', 'data': response})




class UpdateVariant(APIView):
    def post(self, request):
        print("")
        return Response({'Status': 'success'})