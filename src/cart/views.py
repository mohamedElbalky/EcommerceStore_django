from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from store.models import Product, Category
from .cart import Cart
# from .utils import cart_qty


@login_required
def cart_summery(request):
    """display all cart items"""
    cart = Cart(request)
    
    cart_qty = sum(int(item["quantity"]) for item in cart.cart.values())
    transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

    context = {
        "cart_": cart,
        "transport_cost": transport_cost
    }
    return render(request, "cart/summery.html", context)


@login_required
def cart_add(request):
    """add items to the cart"""
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        qty_value = request.POST.get("qty_value")

        product = get_object_or_404(Product, id=product_id)
        product_quantity = product.qty
        # if quanity input less or equal 0 or greter than product_quantity in db
        if (int(qty_value) <= 0) or (int(qty_value) > product_quantity):
            return JsonResponse({"erorr_quantity": str(product_quantity)})


        cart.add(product=product, quantity=qty_value)
        cart_length = cart.__len__()
        response = JsonResponse({"cart_length": cart_length})

        return response


@login_required
def cart_delete(request):
    """delete cart item"""
    cart = Cart(request)
    if request.POST.get("action") == "delete":
        product_id = int(request.POST.get("product_id"))

        cart.delete(product_id=product_id)

        cart_qty = sum(int(item["quantity"]) for item in cart.cart.values())
        transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

        cart_length = cart.__len__()
        cart_total_price = cart.get_total_price()
        return JsonResponse(
            {"cart_length": cart_length, "cart_total_price": cart_total_price, "transport_cost": transport_cost}, 
            )

@login_required
def cart_update(request):
    """update the cart items"""
    cart = Cart(request)
    if request.POST.get("action") == "put":
        product_id = int(request.POST.get("product_id"))
        quantity = request.POST.get("quantity")
        # print(request.POST.get())
        # print(cart.cart)
        product = get_object_or_404(Product, id=product_id)
        product_quantity = product.qty
        # when user enter 0 or number larger than than product qty
        if (int(quantity) <= 0) or (int(quantity) > product_quantity):
            return JsonResponse({"erorr_quantity": str(product_quantity)})

        cart.update(product_id, quantity)

        cart_qty = sum(int(item["quantity"]) for item in cart.cart.values())
        transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

        cart_length = cart.__len__()
        cart_total_price = cart.get_total_price()
        item_total_price = Decimal(cart.cart[str(
            product_id)]["price"]) * Decimal(cart.cart[str(product_id)]["quantity"])
        return JsonResponse({
            "cart_length": cart_length,
            "cart_total_price": cart_total_price,
            "item_total_price": item_total_price,
            "transport_cost": transport_cost
        })
