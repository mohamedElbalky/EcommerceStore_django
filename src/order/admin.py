import csv
import datetime
from django.http import HttpResponse

from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin

from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename = {opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


def order_pdf(obj):
    return format_html('PDF', reverse('order:invoice_pdf', args=[obj.id]))


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ("product",)
    fields = ('product', 'price', 'quantity')
    readonly_fields = ["get_cost"]

def order_detail(obj):
    url = reverse('order:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city',
        'transport', 'created', 'status', order_pdf, order_detail
    ]
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]

    actions = [export_to_csv]


