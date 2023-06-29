from django.urls import path, include
from .import views
from rest_framework import routers
from .views import ProductView, GetConfig, GetProductTypes, CreateProductTypeAttributeValues, GetProductTypeAttributeValues, updateProductTypeAttributeValues

router = routers.DefaultRouter()
# router.register(r'blogs', views.BlogViewSet)
router.register(r'categories/home', views.CategorySet)
router.register(r'categories/all', views.CategoryAllSet)
router.register(r'categories/tree', views.CategoryTreeSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'categories-trash', views.CategoryTrashViewSet)
router.register(r'attributes', views.AttributeViewSet)
router.register(r'attributes-trash', views.AttributeTrashViewSet)
router.register(r'attribute-values', views.AttributeValueViewSet)
router.register(r'product-types', views.ProductTypeViewSet)
router.register(r'product-types-trash', views.ProductTypeTrashViewSet)
router.register(r'product-type-attribute-values', views.ProductTypeAttributeValueViewSet)
router.register(r'shipping-type', views.ShippingTypeViewSet)
router.register(r'shipping-type', views.ShippingTypeViewSet)
router.register(r'cateogry-faq', views.CategoryFAQViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product-csv/', ProductView.as_view()),
    path('get-config/', GetConfig.as_view()),
    path('get-product-filters/', GetProductTypes.as_view()),
    path('create-product-type-attribute-values/', CreateProductTypeAttributeValues.as_view()),
    path('get-product-type-attribute-values/', GetProductTypeAttributeValues.as_view()),
    path('update-product-type-attribute-values/', updateProductTypeAttributeValues.as_view()),
    path('rest-auth/', include('rest_auth.urls'))

]
