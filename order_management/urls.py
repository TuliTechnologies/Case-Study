from django.urls import path, include
from .import views
from rest_framework import routers
from .views import GetOrderDetails, CheckDiscountCoupon, SendProofingMail, GetDeliveryCost
# from .views import CreateTransection
router = routers.DefaultRouter()
router.register(r'create-order', views.CreateOrder)
router.register(r'customer-address', views.CustomerAddressViewSet)
# router.register(r'create_order', views.OrderViewSet)
router.register(r'quotation', views.QuotationView)
router.register(r'shipping-address', views.ShippingAddressView)
router.register(r'billing-address', views.BillingAddressView)
router.register(r'transaction', views.TransactionView)
router.register(r'user-order', views.UserOrder)
router.register(r'user-artworks', views.UserArtworkView)
router.register(r'discount-coupons', views.DiscountCouponView)
router.register(r'order-items', views.OrderItemView)
router.register(r'order-communication', views.OrderCommunicationView)
router.register(r'order-activity', views.OrderActivityView)
router.register(r'artwork-proofing', views.ArtworkProofingView)
router.register(r'saved-cards', views.SavedCardsView)


urlpatterns = [
    path('', include(router.urls)),
    # path('create-transection/', CreateTransection.as_view(), name= 'CreateTransection'),

    path('get-order-details/<int:order_id>/', GetOrderDetails.as_view()),
    path('send-proofing-mail/<int:order_id>/', SendProofingMail.as_view()),
    path('check-coupons/', CheckDiscountCoupon.as_view()),
    path('get-delivery-cost/', GetDeliveryCost.as_view()),

]
