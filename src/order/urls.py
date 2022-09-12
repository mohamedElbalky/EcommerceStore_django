from django.urls import path

from .views import order_create_view, invoice_pdf, admin_order_detail



app_name = "order"


urlpatterns = [
    path("checkout/", order_create_view, name="order_create"),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', invoice_pdf, name='invoice_pdf'),
]
