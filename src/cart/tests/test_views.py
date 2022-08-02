
from multiprocessing.connection import Client
from urllib import response
from wsgiref import headers
from django.test import TestCase, Client

from django.urls import reverse
from django.contrib.auth import get_user_model


from store.models import Product, Category


User = get_user_model()


class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(username="moo", password="123")
        Category.objects.create(name="django")

        # create three products
        Product.objects.create(
            category_id=1,
            created_by_id=1,
            title="django 1",
            price=10.00,
            in_stock=True,
            is_active=True
        )
        Product.objects.create(
            category_id=1,
            created_by_id=1,
            title="django 2",
            price=10.00,
            in_stock=True,
            is_active=True,
            qty=10
        )
        Product.objects.create(
            category_id=1,
            created_by_id=1,
            title="django 3",
            price=20.00,
            in_stock=True,
            is_active=True,
            qty=10
        )

        # add two items to the session
        self.client.post(reverse("cart:cart_add"), {
                         "product_id": 1,
                         "qty_value": "1",
                         "action": "post"
                         },
                         xhr=True)
        self.client.post(reverse("cart:cart_add"), {
                         "product_id": 2,
                         "qty_value": "2",
                         "action": "post"},
                         xhr=True)

    def test_cart_url(self):
        """test cart summery url"""
        response = self.client.get(reverse("cart:cart_summery"))
        self.assertEqual(response.status_code, 200)

    def test_cart_add(self):
        """test cart add view"""
        response = self.client.post(reverse("cart:cart_add"), {
            "product_id": 3,
            "qty_value": "1",
            "action": "post"},
            xhr=True)
        # 1 form 1  +  2 from 2  + 1 from 3
        self.assertEqual(response.json(), {"qty":  4})

    def test_cart_erorr_add(self):
        """test cart add when the quanity is equal to 0 
            or less than 0 or geater than the qty of the product
        """
        response = self.client.post(reverse("cart:cart_add"), {
            "product_id": 1,
            "qty_value": "0",
            "action": "post"},
            xhr=True)
        product_qty = Product.objects.get(id=1).qty
        self.assertEqual(response.json(), {"erorr_quantity": str(product_qty)})

    def test_cart_delete(self):
        """test cart delete view"""
        response = self.client.post(reverse("cart:cart_delete"), {
            "product_id": 1,
            "action": "delete"},
            xhr=True)

        #  (2 from 2) --> 20.00 ==> total 40.00
        self.assertEqual(response.json(),
                         {"cart_length": 2,
                          "cart_total_price": "20.00"})

    def test_cart_update(self):
        """test cart update view"""
        response = self.client.post(reverse("cart:cart_update"),
                                    {"product_id": 2,
                                     "quantity": "1",
                                     "action": "put"
                                     })
        # (1 from 1) --> 10.00 + (1 from 2) --> 10.00 ===> total 20.00
        self.assertEqual(response.json(),
                         {
            "cart_length": 2,
            "cart_total_price": "20.00",
            "item_total_price": "10.00",
        })

    def test_cart_erorr_update(self):
        """test update when the quanity is equal to 0 
            or less than 0 or geater than the qty of the product
        """
        response = self.client.post(reverse("cart:cart_update"),
                                    {"product_id": 2,
                                        "quantity": "0",
                                        "action": "put"
                                     })
        product_qty = Product.objects.get(id=2).qty
        self.assertEqual(response.json(), {"erorr_quantity": str(product_qty)})
