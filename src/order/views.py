from decimal import Decimal

import weasyprint

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

from store.models import Product
from cart.cart import Cart

from .forms  import OrderCreateForm

from .models import Order, OrderItem
from.tasks import order_created



@login_required
def order_create_view(request):
    cart = Cart(request)
    cart_qty = sum(int(item["quantity"]) for item in cart.cart.values())
    transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)
    form = OrderCreateForm()
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            transport = cd.get("transport")
            if transport == "Recipient pickup":
                transport_cost = 0
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.transport_cost = Decimal(transport_cost)

            order.save()
            

            product_ids = cart.cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                cart_item = cart.cart[str(product.pk)]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=cart_item["price"],
                    quantity=cart_item["quantity"]
                )
            cart.cart_clear()

            # launch asyncronous task
            order_created.delay(order.id)
            request.session["order_id"] = order.id
            return redirect(reverse('payment:process'))

            # return render( request, 'order/order_created.html', {'order': order})
    else:
        if request.user.is_authenticated:
            initial_data = {
                "first_name": request.user.first_name,
                "email": request.user.email,
                "telephone": request.user.phone_number,
                "address": request.user.adress_line_1,
                "postal_code": request.user.post_code,
                "country": request.user.countery,
            }
            form = OrderCreateForm(initial=initial_data)
    context = {
        "cart": cart,
        "transport_cost": transport_cost,
        "form": form
    }
    return render(request, "order/order_create.html", context)


# Extending the administration site with custom views

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                    'admin/order/detail.html',
                    {'order': order})







def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    # generate pdf
    html = render_to_string('pdfs/pdf.html', {'order': order})
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'custom/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=stylesheets)
    return response