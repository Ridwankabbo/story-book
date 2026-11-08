# from django.db import models

# # Create your models here.


# class Books(models.Model):
#     title = models.CharField(max_length=200)
#     discription = models.TextField()
#     price=models.DecimalField(max_digits=10, decimal_places=2)
#     book_type = models.CharField(max_length=50)
#     publisher = models.CharField(max_length=100)
#     language=models.CharField(max_length=30)
#     dimensions=models.CharField(max_length=50)
#     amazon_url=models.URLField(max_length=200)
#     cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)

#     def __str__(self):
#         return self.title
    

# class Products(models.Model):
#     name=models.CharField(max_length=100)
#     description=models.TextField()
#     price=models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity=models.IntegerField()
#     material=models.CharField(max_length=100)
#     design=models.CharField(max_length=100)
#     edition=models.CharField(max_length=50)
#     size=models.ChoiceField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=2)


#     def __str__(self):
#         return self.name
    
# class Gadget(models.Model):
#     name = models.CharField(max_length=100)
#     brand = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#     specifications = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     release_date = models.DateField()

#     def __str__(self):
#         return f"{self.brand} {self.model}"

from django.db import models
from django.db.models import JSONField
from apps.account.models import User
import uuid
from decimal import Decimal

class Books(models.Model):
    title = models.CharField(max_length=200)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,blank=True, null=True)
    discription = models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    book_type = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100)
    language=models.CharField(max_length=30)
    video_file = models.FileField(upload_to="videos/files/", null=True, blank=True)
    dimensions=models.CharField(max_length=50)
    stock_quantity=models.IntegerField()
    in_stock = models.BooleanField(default=True, verbose_name="In Stock")
    amazon_url=models.URLField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    guardians = models.ManyToManyField(
        "guardians.Guardian",
        blank=True,
        related_name="books",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title


class BookPhoto(models.Model):
    book = models.ForeignKey(
        Books,
        related_name="photos",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="books/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MissionGallery(models.Model):
    book = models.ForeignKey(
        Books,
        related_name="mission_galleries",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mission Gallery"
        verbose_name_plural = "Mission Galleries"

    def __str__(self):
        return f"{self.title} - {self.book.title}"


class MissionGalleryPhoto(models.Model):
    gallery = models.ForeignKey(
        MissionGallery,
        related_name="photos",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="books/mission_galleries/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mission Gallery Photo"
        verbose_name_plural = "Mission Gallery Photos"

    def __str__(self):
        return f"Photo for {self.gallery.title}"


class Product(models.Model):
    title = models.CharField(max_length=255)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")

    category = models.CharField(
        max_length=100,
        choices=(
            ("gear", "Guardian Gear"),
            ("other", "Others"),
        ),
        blank=True, null=True
    )
    stock_quantity = models.IntegerField()  
    in_stock = models.BooleanField(default=True, verbose_name="In Stock")

    # dynamic attribute storage
    data = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def build_data(self):
        data = {}
        for attr in self.attrs.all():
            if attr.name.lower() == "sizes":
                data["sizes"] = [x.strip() for x in attr.value.split(",")]
            else:
                data[attr.name.lower()] = attr.value
        self.data = data

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)

        if not creating:
            self.build_data()
            super().save(update_fields=["data"])


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name="attrs", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} = {self.value}"



# ------------------------
# ORDER MODEL (Stripe)
# ------------------------
class Order(models.Model):
    BOOK = "book"
    PRODUCT = "product"
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
    )
    order_type = models.CharField(
        max_length=10,
        choices=((BOOK, "Book"), (PRODUCT, "Product"))
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    product_id = models.IntegerField(null=True, blank=True)   # store id of Product OR Book
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    item_uid = models.UUIDField(null=True, blank=True)
    delivery_charge = models.DecimalField(
        max_digits=6, decimal_places=2, default=50
    )

    order_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    stripe_session_id = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    note = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        price = self.price if self.price is not None else Decimal("0")
        quantity = int(self.quantity) if self.quantity is not None else 0
        return price * quantity
    
    def grand_total(self):
        price = self.price if self.price is not None else Decimal("0")
        quantity = int(self.quantity) if self.quantity is not None else 0
        delivery = self.delivery_charge if self.delivery_charge is not None else Decimal("0")
        return price * quantity + delivery

    def __str__(self):
        return f"Order #{self.id}"
    def save(self, *args, **kwargs):
        is_new = self.pk is None

        old_status = None
        if not is_new:
            old_status = Order.objects.get(pk=self.pk).order_status

        super().save(*args, **kwargs)

        if is_new or old_status != self.order_status:
            OrderStatusLog.objects.create(
                order=self,
                status=self.order_status,
                note=f"Status changed to {self.order_status}"
            )


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


# class CartItem(models.Model):
#     BOOK = "book"
#     PRODUCT = "product"

#     cart = models.ForeignKey(
#         Cart, related_name="items", on_delete=models.CASCADE
#     )
#     item_type = models.CharField(
#         max_length=10, choices=((BOOK, "Book"), (PRODUCT, "Product"))
#     )
#     item_id = models.IntegerField()
#     title = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#     extra = models.JSONField(default=dict, blank=True)  # size, color etc

#     def total(self):
#         return self.price * self.quantity
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE
    )

    # 🔥 UUID-based real relation
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )
    object_id = models.UUIDField()
    item = GenericForeignKey("content_type", "object_id")

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    extra = models.JSONField(default=dict, blank=True)

    def total(self):
        return self.price * self.quantity

class OrderStatusLog(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="status_logs",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50,
        choices=Order.STATUS_CHOICES
    )
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Order {self.order.id} → {self.status}"
