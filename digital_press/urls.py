from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pages.urls')),
    path('api/catalog-product/', include('catalog_product.urls')),
    path('api/order/', include('order_management.urls')),
    path('api/supplier/', include('supplier.urls')),
    path('api/studio/', include('studio.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/user/', include('user.urls')),
    path('api/variant/', include('variant.urls')),

    # token based auth
    
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
