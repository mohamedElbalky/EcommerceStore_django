
# from unittest import skip
from errno import ENFILE
from importlib import import_module
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.conf import settings

from ..models import Category, Product
from ..views import all_products_view

# @skip("reason of slipping")
# class SkipTest(TestCase):
#     def test_skip_example(self):
#         pass


class TestViewResponces(TestCase):
    def setUp(self):
        self.c = Client()
        # self.factory = RequestFactory()

        User.objects.create(username="admin")
        self.cat = Category.objects.create(name="django")
        self.pr = Product.objects.create(
            category_id=1,
            created_by_id=1,
            title="django book",
            price=21.45,
            in_stock=True,
            is_active=True
        )

    def test_allowed_host(self):
        response = self.c.get("/", HTTP_HOST="momo.com")
        self.assertEqual(response.status_code, 400)
        response = self.c.get("/", HTTP_HOST="elbalky.com")
        self.assertEqual(response.status_code, 200)

    def test_all_products_url(self):
        """test all products url / """
        res = self.c.get("/")
        self.assertEqual(res.status_code, 200)

    def test_all_products_category_url(self):
        """test all products url /category_slug/ """
        cat_slug = self.cat.slug
        res = self.c.get(f"/{cat_slug}/")
        self.assertEqual(res.status_code, 200)

    def test_product_detail_url_one(self):
        """test url for product detail /item/product_slug/"""
        res = self.c.get(reverse("store:product_detail",
                         kwargs={"slug": "django-book"}))
        self.assertEqual(res.status_code, 200)

    def test_product_detail_url_two(self):
        """test url for product detail /item/product_slug/"""
        res = self.c.get(self.pr.get_absolute_url())
        self.assertEqual(res.status_code, 200)

    def test_product_detail_url_three(self):
        """test url for product detail /item/product_slug/"""
        pro_slug = self.pr.slug
        res = self.c.get(f"/book/{pro_slug}/")
        print(res.reason_phrase)

        self.assertEqual(res.status_code, 200)

    def test_home_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = all_products_view(request)
        html = response.content.decode("'utf8")
        # print(html)
        self.assertTrue(html.startswith("\n<!DOCTYPE html>\n"))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        """test search"""
        res = self.c.get("/search/", {"q": "django"})
        self.assertEqual(res.status_code, 200)

    # def test_using_factory(self):
    #     """using factory in test"""
    #     request = self.factory.get("/")
    #     response = all_products_view(request)
    #     html = response.content.decode("'utf8")
    #     self.assertTrue(html.startswith("\n<!DOCTYPE html>\n"))
    #     self.assertEqual(response.status_code, 200)
