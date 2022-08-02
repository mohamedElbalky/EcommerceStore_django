from .cart import Cart


def cart(request):
    cart = Cart(request)
    return {
        "cart": cart
    }


def cart_length(request):
    cart = Cart(request)
    return {
        "cart_length": len(cart)
    }



