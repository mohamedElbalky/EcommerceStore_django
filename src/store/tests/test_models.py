from itertools import product

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.text import slugify

from ..models import Category, Product


class TestCategoryModel(TestCase):
    """test Category Model functionality"""
    def setUp(self):
        """setup the Category testCase to test it"""
        self.user = User.objects.create(username="admin")
        self.num = 10
        for _ in range(0, self.num):
            Category.objects.create(
                name="django"
            )
        for _ in range(0, self.num):
            Product.objects.create(
            category_id=1,
            created_by_id=1,
            title="django beginners",
            price=12.45,
                )

    def test_category_model(self):
        """test instantiat the category model"""
        instance = Category.objects.all().order_by("id").first()
        self.assertTrue(isinstance(instance, Category))

    def test_name_from_category_model(self):
        """test name field in catogery model"""
        instance = Category.objects.all().order_by("id").first()
        name = instance.name
        self.assertEqual(name, "django")

    def test_slug_field(self):
        """test slug field in product model"""
        instance = Category.objects.all().order_by("id").first()
        product_title = instance.name
        self.assertEqual(instance.slug, slugify(product_title))


    def test_categories_slugs_are_unique(self):
        """test the unique slugs"""
        slugs_list = Category.objects.all().values_list("slug")
        unique_list = list(set(slugs_list))
        self.assertEqual(len(slugs_list), len(unique_list))


    def test_get_products_category_method(self):
        """test get_products_by_category funcrion from models"""
        cat = Category.objects.get(id=1)
        products_for_category = cat.get_products_by_category()
        products_for_category_ = Product.objects.filter(category=cat)
        self.assertEqual(len(products_for_category), len(products_for_category_))


class TestProductModel(TestCase):
    """test Product Model functionality"""
    def setUp(self):
        """setup the product testCase to test it"""
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        self.products_num = 10
        for _ in range(0, self.products_num):
            Product.objects.create(
                category_id=1,
                created_by_id=1,
                title="django beginners",
                price=12.45,
            )

    def test_product_model(self):
        """test product model"""
        instance = Product.objects.all().order_by("id").first()
        self.assertTrue(isinstance(instance, Product))
        self.assertEqual(str(instance), str("django beginners"))

    def test_slug_field(self):
        """test slug field in product model"""
        instance = Product.objects.all().order_by("id").first()
        product_title = instance.title
        self.assertEqual(instance.slug, slugify(product_title))
    

    def test_produts_slugs_are_unique(self):
        """test the unique slugs"""
        slugs_list = Product.objects.all().values_list("slug")
        unique_list = list(set(slugs_list))
        self.assertEqual(len(slugs_list), len(unique_list))

    
