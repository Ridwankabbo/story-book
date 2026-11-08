import stripe,json
from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny as A
from .models import Books, Product, Order, OrderStatusLog, Cart, CartItem
from .serializers import *
stripe.api_key = settings.STRIPE_SECRET_KEY
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# ---------- BOOK APIs ----------

class BookListAPIView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes=[A]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Keep ONLY the fields you want
        data = [
            {
                "id": item["id"],
                "uid": item["uid"],
                "title": item["title"],
                "discription": item["discription"],
                "cover_image": item["cover_image"],
                "in_stock": item.get("in_stock", True),
            }
            for item in serializer.data
        ]

        return Response(data)


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes=[A]


# ---------- PRODUCT APIs ----------

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [A]  # or [A], depending on your need

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True) if hasattr(Product, "is_active") else Product.objects.all()
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Return only the fields you want: id, name, description, price, and photo
        data = [
            {
                "id": item["id"],
                "uid": item["uid"],
                "name": item["title"],  # assuming 'name' corresponds to 'title'
                "description": item["description"],
                "photo": item["image"],  # assuming 'photo' corresponds to 'image'
                "price": item["price"],
                "in_stock": item.get("in_stock", True),
            }
            for item in serializer.data
        ]

        return Response(data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [A]


# ---------- STRIPE CHECKOUT API (BOOK + PRODUCT দুটোই) ----------

class CreateCheckoutSessionAPIViewSingleProduct(APIView):
    """
    POST body:
    {
      "order_type": "book" | "product",
      "id": 12,                 # Book id or Product id
      "quantity": 1,
      "customer_name": "Riyad",
      "email": "test@test.com",
      "address": "Dhaka",
      "city": "Dhaka",
      "country": "Bangladesh"
    }
    """

    def post(self, request):
        uid = request.data.get("uid")
        quantity = int(request.data.get("quantity", 1))
        note = request.data.get("note", "")

        try:
            item = Books.objects.get(uid=uid)
            order_type = Order.BOOK
        except Books.DoesNotExist:
            item = get_object_or_404(Product, uid=uid)
            order_type = Order.PRODUCT

        order = Order.objects.create(
            order_type=order_type,
            product_id=item.id,
            user=request.user,
            item_uid=item.uid,
            title=item.title,
            price=item.price,
            quantity=quantity,
            note=note,   # 👈 size / color / message
            customer_name=request.data.get("customer_name"),
            email=request.data.get("email"),
            address=request.data.get("address"),
            city=request.data.get("city"),
            country=request.data.get("country"),
        )


        # Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.title},
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": quantity,
                },
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Delivery Charge"},
                        "unit_amount": 5000,  # 50 USD * 100
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.FRONTEND_SUCCESS_URL,  # e.g. https://yourdomain.com/success
            cancel_url=settings.FRONTEND_CANCEL_URL,    # e.g. https://yourdomain.com/cancel
        )

        order.stripe_session_id = checkout_session.id
        order.save()

        return Response(
            {
                "checkout_url": checkout_session.url,
                "order_id": order.id,
            },
            status=status.HTTP_201_CREATED,
        )

class CreateCheckoutSessionAPIViewForCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if not cart.items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        line_items = []
        orders = []

        for item in cart.items.all():
            size = item.extra.get("size")
            note = f"Size: {size}" if size else ""

            # Determine order type and product_id from cart item
            try:
                product_obj = Books.objects.get(uid=item.object_id)
                order_type = Order.BOOK
                product_id = product_obj.id
            except Books.DoesNotExist:
                product_obj = Product.objects.get(uid=item.object_id)
                order_type = Order.PRODUCT
                product_id = product_obj.id

            order = Order.objects.create(
                order_type=order_type,
                user=request.user,
                product_id=product_id,                 # ✅ Store actual product ID
                item_uid=item.object_id,          # ✅ UUID goes here
                title=item.title,
                price=item.price,
                quantity=item.quantity,
                note=note,
                customer_name=request.data.get("customer_name"),
                email=request.data.get("email"),
                address=request.data.get("address"),
                city=request.data.get("city"),
                country=request.data.get("country"),
            )




            orders.append(order)

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item.title},
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            })

        # Delivery charge (once)
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Delivery Charge"},
                "unit_amount": 5000,
            },
            "quantity": 1,
        })

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=settings.FRONTEND_SUCCESS_URL,
            cancel_url=settings.FRONTEND_CANCEL_URL,
        )

        for order in orders:
            order.stripe_session_id = session.id
            order.save(update_fields=["stripe_session_id"])

        cart.items.all().delete()

        return Response(
            {
                "checkout_url": session.url,
                "order_ids": [o.id for o in orders],
            },
            status=status.HTTP_201_CREATED
        )


# ---------- STRIPE WEBHOOK (BOOK + PRODUCT common) ----------
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookAPIView(APIView):
    permission_classes = [A]
    authentication_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            # ✅ ALWAYS filter (works for single + cart)
            orders = Order.objects.filter(
                stripe_session_id=session["id"]
            )

            for order in orders:
                # 🔒 idempotency guard
                if order.paid:
                    continue

                order.paid = True
                order.order_status = Order.STATUS_PAID
                order.save(update_fields=["paid", "order_status"])

                OrderStatusLog.objects.create(
                    order=order,
                    status=Order.STATUS_PAID,
                    note="Payment received"
                )

                # stock reduction
                if order.order_type == Order.BOOK:
                    book = Books.objects.get(id=order.product_id)
                    book.stock_quantity -= order.quantity
                    book.save(update_fields=["stock_quantity"])
                else:
                    product = Product.objects.get(id=order.product_id)
                    product.stock_quantity -= order.quantity
                    product.save(update_fields=["stock_quantity"])

        return HttpResponse(status=200)



# ---------- ORDER VIEW APIs (customer) ----------

from django.contrib.contenttypes.models import ContentType

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        uid = request.data.get("uid")
        quantity = int(request.data.get("quantity", 1))
        extra = request.data.get("extra", {})

        try:
            item = Books.objects.get(uid=uid)
        except Books.DoesNotExist:
            item = get_object_or_404(Product, uid=uid)

        content_type = ContentType.objects.get_for_model(item)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=content_type,
            object_id=item.uid,
            defaults={
                "title": item.title,
                "price": item.price,
                "quantity": quantity,
                "extra": extra,
            },
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=201)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)
class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = request.user.cart
        CartItem.objects.filter(cart=cart, id=item_id).delete()
        return Response(CartSerializer(cart).data)

class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, cart_item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=cart_item_id,
            cart__user=request.user
        )

        quantity = request.data.get("quantity")
        extra = request.data.get("extra")

        # update quantity
        if quantity is not None:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {"detail": "Quantity must be greater than zero"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = quantity

        # update extras (size, color etc.)
        if isinstance(extra, dict):
            cart_item.extra = extra

        cart_item.save()

        return Response(
            {
                "id": cart_item.id,
                "title": cart_item.title,
                "price": str(cart_item.price),
                "quantity": cart_item.quantity,
                "extra": cart_item.extra,
                "line_total": cart_item.total(),
            },
            status=status.HTTP_200_OK
        )

class OrderTimelineAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response(
                {"detail": "session_id is required"},
                status=400
            )

        orders = Order.objects.filter(
            stripe_session_id=session_id,
            user=request.user
        )

        if not orders.exists():
            return Response(
                {"detail": "Order group not found"},
                status=404
            )

        logs = (
            OrderStatusLog.objects
            .filter(order__in=orders)
            .order_by("created_at")
        )

        timeline = []
        seen_status = set()

        for log in logs:
            # avoid duplicate status rows
            if log.status in seen_status:
                continue

            seen_status.add(log.status)

            timeline.append({
                "status": log.status,
                "note": log.note,
                "created_at": log.created_at.isoformat(),
            })

        return Response({
            "order_group_id": session_id,
            "current_status": orders.first().order_status,
            "timeline": timeline,
        })



from rest_framework.exceptions import NotFound
class MyOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related("status_logs")
            .order_by("-created_at")
        )

        grouped = {}

        for order in orders:
            group_id = order.stripe_session_id or f"single-{order.id}"

            if group_id not in grouped:
                grouped[group_id] = {
                    "order_group_id": group_id,
                    "created_at": order.created_at,
                    "items": [],
                    "latest_log": None,   # 👈 we track this
                }

            # 🔹 product image
            if order.order_type == Order.BOOK:
                obj = Books.objects.filter(id=order.product_id).first()
                if not obj:
                    image = None
                else:
                    first_photo = obj.photos.filter(image__isnull=False).first()
                    image = (
                        first_photo.image.url
                        if first_photo and first_photo.image
                        else None
                    )
            else:
                obj = Product.objects.filter(id=order.product_id).first()
                image = obj.image.url if obj and obj.image else None

            grouped[group_id]["items"].append({
                "order_id": order.id,
                "title": order.title,
                "price": float(order.price),
                "quantity": order.quantity,
                "note": order.note,
                "image": image,
            })

            # 🔥 determine latest log per group
            for log in order.status_logs.all():
                current_latest = grouped[group_id]["latest_log"]

                if (
                    current_latest is None
                    or log.created_at > current_latest.created_at
                ):
                    grouped[group_id]["latest_log"] = log

        # 🔁 finalize response
        response = []

        for group in grouped.values():
            log = group["latest_log"]

            response.append({
                "order_group_id": group["order_group_id"],
                "created_at": group["created_at"],
                "latest_status": log.status if log else None,
                "latest_status_note": log.note if log else "",
                "latest_status_date": (
                    log.created_at.strftime("%d %b %Y")
                    if log else None
                ),
                "items": group["items"],
            })

        return Response(response)

class OrderProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(
                id=order_id, user=request.user
            )
        except Order.DoesNotExist:
            raise NotFound("Order not found")

        return Response({
            "order_id": order.id,
            "status": order.order_status,
            "timeline": [
                {"label": "Order Placed", "done": True},
                {"label": "Payment Completed", "done": order.paid},
                {"label": "Shipped", "done": order.order_status in ["shipped", "delivered"]},
                {"label": "Delivered", "done": order.order_status == "delivered"},
            ],
        })