def cart_qty(request):
    cart = request.session.get("cart_key")
    cart_keys = cart.keys()
    total_qty = 0
    for key in cart_keys:
        product_qty = cart[key]["quantity"]
        total_qty += int(product_qty)
    return  total_qty

        