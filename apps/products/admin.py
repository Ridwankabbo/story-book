from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# class ProductAttributeInline(admin.TabularInline):
#     model = ProductAttribute
#     extra = 1


class BookPhotoInline(admin.TabularInline):
    model = BookPhoto
    extra = 1


class MissionGalleryPhotoInline(admin.TabularInline):
    model = MissionGalleryPhoto
    extra = 1


@admin.register(MissionGallery)
class MissionGalleryAdmin(ModelAdmin):
    list_display = ["title", "book", "created_at"]
    inlines = [MissionGalleryPhotoInline]


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    # inlines = [ProductAttributeInline]
    list_display = ["title", "category", "price", "in_stock"]
    list_editable = ["in_stock"]

@admin.register(Books)
class BooksAdmin(ModelAdmin):
    list_display = ["title", "publisher", "price", "order", "in_stock"]
    list_editable = ["order", "in_stock"]
    inlines = [BookPhotoInline]
    filter_horizontal = ["guardians"]

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["id", "title", "order_status", "paid", "grand_total", "created_at"]
    list_filter = ["order_status", "paid"]
    readonly_fields = ["grand_total"]

    def save_model(self, request, obj, form, change):
        """
        When admin updates status of one order,
        apply same status to all orders in the same group.
        """
        if not change:
            super().save_model(request, obj, form, change)
            return

        old_obj = Order.objects.get(pk=obj.pk)

        # If status didn't change → normal save
        if old_obj.order_status == obj.order_status:
            super().save_model(request, obj, form, change)
            return

        # ✅ GROUP UPDATE
        if obj.stripe_session_id:
            group_orders = Order.objects.filter(
                stripe_session_id=obj.stripe_session_id
            )
        else:
            # single product order fallback
            group_orders = Order.objects.filter(pk=obj.pk)

        for order in group_orders:
            if order.order_status != obj.order_status:
                order.order_status = obj.order_status
                order.save(update_fields=["order_status"])

                OrderStatusLog.objects.create(
                    order=order,
                    status=obj.order_status,
                    note=f"Status changed to {obj.order_status} by admin"
                )

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["user", "created_at"]
@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ["cart", "price", "title","quantity"]


@admin.register(OrderStatusLog)
class OrderStatusLogAdmin(ModelAdmin):
    pass


