from django.urls import path, include
from .import views
from rest_framework import routers
from .views import ProductVariantSet, GetCatalogProduct, FilterPricing, GetProductVariant, UpdateProductVariant

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'products-trash', views.ProductTrashViewSet)
router.register(r'product-images', views.ProductImagesViewSet)
router.register(r'artworks', views.ArtworksViewSet)
router.register(r'product-design', views.ProductDesignViewSet)
router.register(r'product-variant', views.ProductVariantViewSet)
router.register(r'shipping-details', views.ShippingDetailViewSet)
router.register(r'variant-images', views.VariantsImageViewSet)
router.register(r'product-price-configration', views.ProductPriceConfigrationViewSet)
router.register(r'supplier-product', views.SupplierProductViewSet)
router.register(r'design-service', views.DesignServiceViewSet)
router.register(r'delivery-methods', views.DeliveryMethodsViewSet)
router.register(r'delivery-settings', views.DeliverySettingsViewSet)
router.register(r'faq', views.FAQViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-product-variant/', ProductVariantSet.as_view()),
    path('get-product-variant/<int:product_id>/', GetProductVariant.as_view()),
    path('update-product-variant/<int:product_id>/', UpdateProductVariant.as_view()),
    path('get-catalog-product/<int:product_id>/', GetCatalogProduct.as_view()),
    path('filter-pricing', FilterPricing.as_view()),

]
