from rest_framework import serializers
from .models import *
from apps.guardians.models import Guardian


class MissionGalleryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionGalleryPhoto
        fields = ["id", "image"]


class MissionGallerySerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = MissionGallery
        fields = ["id", "title", "photos", "created_at"]

    def get_photos(self, obj):
        photos = obj.photos.all()[:3]
        return MissionGalleryPhotoSerializer(photos, many=True, context=self.context).data


class BookGuardianSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Guardian
        fields = [
            "id",
            "name",
            "age",
            "about",
            "description",
            "second_description",
            "nationality",
            "roll_number",
            "personality",
            "strengths",
            "weaknesses",
            "aspirational_angle",
            "codename",
            "profile_photo",
        ]

    def get_profile_photo(self, obj):
        request = self.context.get("request")
        photos = []
        for photo in obj.photos.all():
            if photo.profile_photo:
                url = photo.profile_photo.url
                if request:
                    url = request.build_absolute_uri(url)
                photos.append(url)
        return photos


class BookSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    mission_galleries = serializers.SerializerMethodField()
    guardians = BookGuardianSerializer(many=True, read_only=True)
    class Meta:
        model = Books
        fields = [
            "id","uid", "title", "discription", "price",
            "book_type", "publisher", "language",
            "dimensions", "stock_quantity",
            "amazon_url", "cover_image","video_file",
            "mission_galleries", "guardians", "in_stock",
        ]

    def get_cover_image(self, obj):
        urls = [
            photo.image.url
            for photo in obj.photos.all()
            if photo.image
        ]
        return urls[:3]
    def get_mission_galleries(self, obj):
        gallery = obj.mission_galleries.first()

        if not gallery:
            return None

        return MissionGallerySerializer(
            gallery,
            context=self.context
        ).data


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    attrs = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id","uid", "title", "subtitle", "description",
            "price", "image", "category", "stock_quantity",
            "data", "attrs", "created_at", "in_stock",
        ]


class OrderSerializer(serializers.ModelSerializer):
    total_product_price = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "item_uid",
            "order_type",       # "book" or "product"
            "product_id",
            "title",
            "price",
            "quantity",
            "delivery_charge",
            "order_status",
            "grand_total",
            "total_product_price",
            "customer_name",
            "email",
            "address",
            "city",
            "country",
            "paid",
            "created_at",
        ]

    def get_total_product_price(self, obj):
        return obj.total()


    def get_grand_total(self, obj):
        return obj.grand_total()

class CartItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "title",
            "price",
            "quantity",
            "extra",
            "total",
            "product_image",
        ]

    def get_total(self, obj):
        return obj.total()

    def get_product_image(self, obj):
        # Use object_id (UUID) to find the item directly
        try:
            # Try Books first
            book = Books.objects.get(uid=obj.object_id)
            first_photo = book.photos.filter(image__isnull=False).first()
            return first_photo.image.url if first_photo and first_photo.image else None
        except Books.DoesNotExist:
            pass
        
        try:
            # Try Product
            product = Product.objects.get(uid=obj.object_id)
            return product.image.url if product.image else None
        except Product.DoesNotExist:
            pass
        
        return None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    sub_total = serializers.SerializerMethodField()
    delivery_charge = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "sub_total", "delivery_charge", "grand_total"]

    def get_sub_total(self, cart):
        return sum(item.total() for item in cart.items.all())

    def get_delivery_charge(self, cart):
        return 50  # fixed

    def get_grand_total(self, cart):
        return self.get_sub_total(cart) + 50
class OrderListSerializer(serializers.ModelSerializer):
    latest_status = serializers.SerializerMethodField()
    latest_status_note = serializers.SerializerMethodField()
    latest_status_date = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "title",
            "price",
            "quantity",
            "note",
            "latest_status",
            "latest_status_note",
            "latest_status_date",
            "product_image",
        ]

    def _get_last_log(self, obj):
        return obj.status_logs.last()

    def get_latest_status(self, obj):
        last_log = self._get_last_log(obj)
        return last_log.status if last_log else obj.order_status

    def get_latest_status_note(self, obj):
        last_log = self._get_last_log(obj)
        return last_log.note if last_log else ""

    def get_latest_status_date(self, obj):
        last_log = self._get_last_log(obj)
        return (
            last_log.created_at.strftime("%d %b %Y")
            if last_log else None
        )

    def get_product_image(self, obj):
        if obj.order_type == Order.BOOK:
            book = Books.objects.filter(id=obj.product_id).first()
            if not book:
                return None
            first_photo = book.photos.filter(image__isnull=False).first()
            return first_photo.image.url if first_photo and first_photo.image else None
        else:
            product = Product.objects.filter(id=obj.product_id).first()
            return product.image.url if product and product.image else None
