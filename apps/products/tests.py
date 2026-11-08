from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.products.models import Books, Product

class StockStatusAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Books.objects.create(
            title="Test Book",
            discription="Description",
            price=15.00,
            book_type="Paperback",
            publisher="Test Publisher",
            language="English",
            dimensions="8x10",
            stock_quantity=10,
            amazon_url="https://amazon.com"
        )
        self.product = Product.objects.create(
            title="Test Product",
            description="Product Description",
            price=25.00,
            image="test.jpg",
            category="gear",
            stock_quantity=5
        )

    def test_default_in_stock(self):
        # Default value of in_stock should be True
        self.assertTrue(self.book.in_stock)
        self.assertTrue(self.product.in_stock)

    def test_book_list_api(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify in_stock is in the response dictionary list
        data = response.data["data"]["data"]
        self.assertTrue(data[0]["in_stock"])

    def test_book_detail_api(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]
        self.assertTrue(data["in_stock"])

    def test_product_list_api(self):
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]["data"]
        self.assertTrue(data[0]["in_stock"])

    def test_product_detail_api(self):
        response = self.client.get(reverse("product-detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]
        self.assertTrue(data["in_stock"])

    def test_stock_toggle_off(self):
        # Toggle stock off
        self.book.in_stock = False
        self.book.save()
        self.product.in_stock = False
        self.product.save()

        # Check detail views
        response_book = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertFalse(response_book.data["data"]["in_stock"])

        response_product = self.client.get(reverse("product-detail", kwargs={"pk": self.product.pk}))
        self.assertFalse(response_product.data["data"]["in_stock"])

