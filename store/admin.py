from django.contrib import admin
from .models import Collection, Product, Customer, Order

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name']
    list_per_page = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', 'slug']
    list_editable = ['unit_price', 'inventory', 'slug']
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    ordering = ['id']
    list_select_related = ['customer']
    list_per_page = 10


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['title']
    list

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)