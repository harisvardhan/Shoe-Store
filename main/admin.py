from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_item_total']
    search_fields = ['product__name']

    def get_item_total(self, obj):
        return f"${obj.get_item_total()}"
    get_item_total.short_description = 'Item Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_item_total']
    search_fields = ['product__name']

    def get_item_total(self, obj):
        return f"${obj.get_item_total()}"
    get_item_total.short_description = 'Item Total'
