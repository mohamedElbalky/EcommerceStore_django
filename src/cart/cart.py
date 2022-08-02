from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    """
    A base class, providing some default behaviors
    that can be inherited or pverrieded, as necessary
    """

    def __init__(self, request):
        """initial session and add cart_key if not exists"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if "cart_key" not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity):
        """add and update the user's cart"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "price": str(product.price),
                "quantity": int(quantity)
            }
        else:
            self.cart[product_id]["quantity"] = int(quantity)


        self.save()

    def save(self):
        """save data to session"""
        self.session.modified = True

    def __len__(self):
        """return the number of product in cart"""
        return sum(int(item["quantity"]) for item in self.cart.values())

    def __iter__(self):
        """return all products in the cart"""
        products_ids = self.cart.keys()
        # print(products_ids)

        # filer the products by the list of keys in the cart
        products = Product.objects.filter(id__in=products_ids)

        # make copy from the cart to display it in templates
        cart = self.cart.copy()

        for product in products:
            # make str(product.id) becouse jason store data as strings
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * Decimal(item["quantity"])
            # use yield to return all products when use __iter__ --> |length in template
            yield item

    def get_total_price(self):
        """return the total price of all products in the cart"""
        total_price = sum(Decimal(item["price"]) * Decimal(item["quantity"])
                          for item in self.cart.values())
        return total_price

    def delete(self, product_id):
        if str(product_id) in self.cart:
            # print(product_id)
            del self.cart[str(product_id)]
            self.save()

    def update(self, product_id, quantity):
        if str(product_id) in self.cart:
            self.cart[str(product_id)]["quantity"] = quantity
            self.save()

