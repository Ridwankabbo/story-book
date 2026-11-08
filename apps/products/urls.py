from django.urls import path
from .views import *

urlpatterns = [
    # books
    path("books/", BookListAPIView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailAPIView.as_view(), name="book-detail"),

    # products
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),

    # checkout
    path("checkout/create-session/", CreateCheckoutSessionAPIViewSingleProduct.as_view(), name="create-checkout"),
    path("checkout/cart-session/", CreateCheckoutSessionAPIViewForCart.as_view(), name="create-checkout"),

    # webhook (Stripe will call this)
    path("stripe/webhook/", StripeWebhookAPIView.as_view(), name="stripe-webhook"),

    # order
    path("orders/", MyOrdersAPIView.as_view()),
    path("orders/<int:order_id>/progress/", OrderProgressAPIView.as_view()),
    path("orders/timeline/", OrderTimelineAPIView.as_view()),

    path("cart/", CartAPIView.as_view()),
    path("cart/add/", AddToCartAPIView.as_view()),
    path("cart/items/<int:cart_item_id>/", UpdateCartItemAPIView.as_view(),),
    path("cart/remove/<int:item_id>/", RemoveCartItemAPIView.as_view()),
]
#for check