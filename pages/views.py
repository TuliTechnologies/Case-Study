from rest_framework import viewsets
from . serializers import *
from . models import *
from catalog_product.models import ProductPriceConfigrations, Products
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, UnsupportedMediaType, NotAcceptable
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
import numpy as np
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import filters
from catalog_product.serializers import ProductSerializer

class CategorySet(viewsets.ModelViewSet):
    queryset = Categories.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_trash']

    def list(self, request):
        queryset = Categories.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at').values()
        resultant = [
            {
                "title": "Home",
                "type": "sub",
                "badgeValue": "new",
                "active": "false"},
            {
                "title": "Shop all product",
                "type": "sub",
                "active": "false"
            },
            {
                "title": "Advise and help ",
                "type": "sub",
                "active": "false"
            }
        ]

        parentCategoryList = []
        childCategoryList = []
        for data in queryset:
            if data['parent'] == None:
                parentCategoryList.append(data)

            else:

                childCategoryList.append(data)
            subCategory = []

            for parent in parentCategoryList:
                for child in childCategoryList:
                    if child['parent'] == parent['id']:
                        subCategory.append(child)
                        final_child = []
                        for sub in subCategory:
                            if sub['parent'] == parent['id']:
                                final_child.append(sub)
                                parent['children'] = final_child

        # adding path #
        for data in childCategoryList:
            path_id = data['id']
            name = data['name']
            data['path'] = f'/category/{path_id}'
            data['title'] = name

        for data in parentCategoryList:
            path_id = data['id']
            name = data['name']
            data['path'] = f'/category/{path_id}'
            data['title'] = name

        # adding children #
        final_data = resultant[1]

        final_data['children'] = parentCategoryList

        # add Additional response for a to z category
        all_data = []

        # Category List
        category_list = Categories.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at').values()

        for category in category_list:
            all_data.append(
                {'name': category['name'],  'id': category['id'], 'type': 'category'})
            print("category", category)

        # Product List
        product_list = Products.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False) and Q(show_a_to_z_category=True)).order_by('-updated_at').values()

        for product in product_list:
            all_data.append(
                {'id': product['id'], 'name': product['short_name'], 'type': 'product'})
            # print("category", category)

        return Response({'status': 'success', 'results': resultant, 'a_to_z_category': all_data})


class CategoryTreeSet(viewsets.ModelViewSet):

    queryset = Categories.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = CategorySerializer

    def retrieve(self, request, pk=None):
        queryset = Categories.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False) and Q(pk=pk)).order_by('-updated_at').values().first()

        child = Categories.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False) and Q(parent=pk)).order_by('-updated_at').values()

        product = Products.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False) and Q(category=pk)).order_by('-updated_at')
        
        product_list = []
        for data in product:
            serializer = ProductSerializer(data).data
            product_list.append(serializer)

        queryset['product_data'] = product_list
        queryset['children'] =  child
        
        return Response({'status': 'success', 'results': queryset})



class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Categories.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = CategorySerializer

    def list(self, request):
        print("PPPP")
        queryset = Categories.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at').values()
        # print('queryset', queryset)
        parentCategoryList = []
        childCategoryList = []
        for data in queryset:
            if data['parent'] == None:
                parentCategoryList.append(data)

            else:

                childCategoryList.append(data)
                # print('*************************',childCategoryList)
            subCategory = []

            for parent in parentCategoryList:
                for child in childCategoryList:
                    if child['parent'] == parent['id']:
                        subCategory.append(child)
                        final_child = []
                        for sub in subCategory:
                            if sub['parent'] == parent['id']:
                                final_child.append(sub)
                                parent['child'] = final_child

        return Response({'status': 'success', 'results': parentCategoryList})

    def retrieve(self, request, pk=None):

        print("AAAAA")
        queryset = Categories.objects.filter(
            Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at').values()
        resultant = {}

        parentCategoryList = []
        childCategoryList = []
        for data in queryset:
            if data['parent'] == None:
                parentCategoryList.append(data)

            else:

                childCategoryList.append(data)
            subCategory = []

            for parent in parentCategoryList:
                for child in childCategoryList:
                    if child['parent'] == parent['id']:
                        subCategory.append(child)
                        final_child = []
                        for sub in subCategory:
                            if sub['parent'] == parent['id']:
                                final_child.append(sub)
                                parent['children'] = final_child

        # adding path #
        for data in childCategoryList:
            path_id = data['id']
            name = data['name']
            data['path'] = f'/category/{path_id}'
            data['title'] = name

        for data in parentCategoryList:
            path_id = data['id']
            name = data['name']
            data['path'] = f'/category/{path_id}'
            data['title'] = name

        # adding children #
        final_data = resultant

        final_data['children'] = parentCategoryList

        for category in resultant['children']:
            if int(pk) == category['id']:
                return Response(category)
        
        return Response(resultant)


class CategoryAllSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Categories.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']


class CategoryTrashViewSet(viewsets.ModelViewSet):

    queryset = Categories.objects.filter(
        Q(is_deleted=False) and Q(is_trash=True)).order_by('-updated_at')
    serializer_class = CategorySerializer


class AttributeViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Attributes.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = AttributeSerializer


class AttributeTrashViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Attributes.objects.filter(
        Q(is_deleted=False) and Q(is_trash=True)).order_by('-updated_at')
    serializer_class = AttributeSerializer


class AttributeValueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = AttributeValues.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = AttributeValueSerializer


class ProductTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ProductTypes.objects.filter(
        Q(is_deleted=False) and Q(is_trash=False)).order_by('-updated_at')
    serializer_class = ProductTypeSerializer

    def retrieve(self, request, pk=None):
        try:
            # get product type
            product_type = ProductTypes.objects.filter(
                Q(is_deleted=False) & Q(id=pk)).values()
            if not product_type.exists():
                return Response({'status': 'error', 'message': 'Product Type not found'}, status=404)
            output = product_type[0]

            # get product type attribute value
            product_type_attribute_value = ProductTypeAttributeValue.objects.filter(
                Q(is_deleted=False) & Q(product_type_id=pk)).values_list('attribute_id', flat=True).distinct()

            attribute_dist = []
            # product_type_attribute_value
            for values in product_type_attribute_value:

                serializer = AttributeSerializer(Attributes.objects.filter(
                    Q(is_deleted=False) & Q(id=values)), many=True)
                attribute_dist.append(serializer.data[0])

            output.update({'attributes': attribute_dist})
            return Response(output)
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)


class ProductTypeTrashViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = ProductTypes.objects.filter(
        Q(is_deleted=False) and Q(is_trash=True)).order_by('-updated_at')
    serializer_class = ProductTypeSerializer

class CategoryFAQViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = CategoryFAQ.objects.filter(
        Q(is_deleted=False) and Q(is_trash=True)).order_by('-updated_at')
    serializer_class = ProductTypeSerializer


class ProductTypeAttributeValueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ProductTypeAttributeValue.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ProductTypeAttributeValueSerializer


class ShippingTypeViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = ShippingType.objects.filter(
        Q(is_deleted=False)).order_by('-updated_at')
    serializer_class = ShippingTypeSerializer


class CreateProductTypeAttributeValues(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            for attribute in data['product_type_values']:
                # print('attribute', attribute)
                for attribute_value in attribute['attribute_value_id']:
                    dict_data = {'attribute_value_id': attribute_value, 'attribute_id':
                                 attribute['attribute_id'], 'product_type_id': data['product_type_id']}
                    product_obj = ProductTypeAttributeValue.objects.create(
                        **dict_data)
                    product_obj.save()

            return Response({'Status': 'Created'})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)


class GetProductTypeAttributeValues(APIView):
    def post(self, request, format=None):
        try:
            data = request.data

            response_data = {}
            response_data['product_type_id'] = data['product_type_id']
            product_type_values = []
            product_type_attribute_value = ProductTypeAttributeValue.objects.filter(
                Q(is_deleted=False) and Q(product_type=data['product_type_id'])).values()

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
            print("product_type_values", product_type_values)
            return Response({'Status': 'Success', 'response': response_data})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)
class updateProductTypeAttributeValues(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            for source in data['old_data']['product_type_values']:
                ProductTypeAttributeValue.objects.filter(pk=source['product_type_attribute_value']).delete()


            # create new
            for attribute in data['product_type_values']:
            # print('attribute', attribute)
                for attribute_value in attribute['attribute_value_id']:
                    dict_data = {'attribute_value_id': attribute_value, 'attribute_id':
                                attribute['attribute_id'], 'product_type_id': data['product_type_id']}
                    product_obj = ProductTypeAttributeValue.objects.create(
                        **dict_data)
                    product_obj.save()
                
                    
            return Response({'Status': 'Updated', 'data': data['product_type_values']})
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=500)


class ProductView(APIView):
    def put(self, request, format=None):
        # try:
        if 'file' not in request.data:
            raise ParseError("Empty content")

        data_file = request.FILES['file']
        print('data_file', data_file)
        file_name = data_file.name
        file_extention = file_name.split('.')[-1]

        allowed_extentions = ['csv', 'xlsx']
        if file_extention not in allowed_extentions:
            raise ParseError('invalid file format.')

        skiprows = 6

        if file_extention == 'xlsx':
            df = pd.read_excel(data_file, skiprows=skiprows)

        # if file_extention == 'csv':
        #     df = pd.read_excel(data_file, skiprows=skiprows)

        else:
            raise UnsupportedMediaType('invalid file type')

        df = df.replace({np.nan: None})

        # print('df', df)

        product_columns = ['PRODUCT SPEC', 'PRODUCT DESCRIPTION', 'PRODUCT TYPE',
                           'CODE', 'SIZE', 'PRINT', 'LEAD TIME', 'CARRIAGE']

        price_columns = {
            'A': {
                'min_qty': 1,
                'max_qty': 5
            },
            'B': {
                'min_qty': 6,
                'max_qty': 11
            },
            'C': {
                'min_qty': 12,
                'max_qty': 25
            },
            'D': {
                'min_qty': 26,
                'max_qty': 49
            },
            'E': {
                'min_qty': 50,
                'max_qty': None
            }
        }

        counter = 0
        mapped_table_dict = {
            'PRODUCT SPEC': 'name',
                            'PRODUCT DESCRIPTION': 'description',
                            'CODE': 'code',
                            'SIZE': 'size',
                            'PRODUCT TYPE': 'type',
                            'PRINT': 'print_area',
                            'LEAD TIME': 'lead_time',
                            'CARRIAGE': 'carriage',
        }

        for index, row in df.iterrows():
            print('row', row)
            dict_data = {}
            for c_name in product_columns:
                # print('c_name', c_name)
                if hasattr(row, c_name):
                    if row[c_name] is None:
                        continue
                    dict_data.update({c_name: row[c_name]})
            if dict_data:
                dict_data = dict((mapped_table_dict[key], value) for (
                    key, value) in dict_data.items())
                print('dict_data', dict_data)

            product_obj, prd_obj_created = Products.objects.get_or_create(
                **dict_data)

            price_dict = {}
            for key, val in price_columns.items():
                if hasattr(row, key):
                    price_dict.update(
                        {'product_id': product_obj, 'price': row[key]})
                    price_dict.update(val)

                price, created = ProductPriceConfigrations.objects.get_or_create(
                    **price_dict)

            if not prd_obj_created:
                print('SupplierProduct Exists.. at ID ->',
                      product_obj.id)
                counter += 1
                continue
            product_obj.save()

        data = {'message': str(counter)+' Objects Created'}
        return Response(data, 200)


class GetConfig(APIView):
    def get(self, request, format=None):
        print_type = request.query_params.get('print_type')
        product_type = request.query_params.get('product_type')

        if not product_type:
            raise NotAcceptable('product_type required...')

        products = Products.objects

        if product_type:
            products = products.filter(name__icontains=product_type)

        if print_type:
            products = products.filter(print_area=print_type)

        products = products.all()

        product_list = []
        for prod in products:
            rows = []
            for p in prod.productpriceconfigrations_set.all():
                qty = f'{p.min_qty}-{p.max_qty}' if p.max_qty else f'{p.min_qty}+'
                rows.append({'qty': qty, 'price': p.price})

            product_list.append({'size': prod.size, 'column': rows})

        data = ProductSerializer(products, many=True).data

        return Response({
            'count': len(product_list),
            'data': product_list
        }, 200)


class GetProductTypes(APIView):

    def get(self, request, format=None):

        product_type = Products.objects.values_list(
            'type', flat=True).distinct().all()
        print_type = Products.objects.values_list(
            'print_area', flat=True).distinct().all()

        product_type = [p for p in product_type if p is not None]
        print_type = [p for p in print_type if p is not None]

        return Response({'product_type': product_type, 'print_type': print_type}, 200)
