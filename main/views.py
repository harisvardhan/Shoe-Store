from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Product, Category, Cart, CartItem, Order, OrderItem

# Home view - show featured products
def home(request):
    featured_products = Product.objects.filter(is_active=True)[:8]
    context = {
        'products': featured_products
    }
    return render(request, 'index.html', context)

# Products listing view
def products(request):
    category = request.GET.get('category')
    products = Product.objects.filter(is_active=True)
    
    if category:
        products = products.filter(category__name=category)
    
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'products.html', context)

# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'product_detail.html', context)

# Stock view
def stock(request):
    return render(request, 'stock.html')

# About us view
def aboutus(request):
    return render(request, 'aboutus.html')

# Contact view
def contact(request):
    return render(request, 'contact.html')


# Cart Views - PHASE 3
@login_required(login_url='/login/')
def get_or_create_cart(request):
    """Get or create cart for current user"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return redirect('view_cart')


@login_required(login_url='/login/')
def view_cart(request):
    """View shopping cart"""
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price()
    }
    return render(request, 'cart.html', context)


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('view_cart')


@login_required(login_url='/login/')
def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        return redirect('view_cart')
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        phone = request.POST.get('phone')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            shipping_address=shipping_address,
            phone=phone,
            status='pending'
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Reduce product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price(),
        'user_phone': request.user.profile.phone if hasattr(request.user, 'profile') else ''
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='/login/')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'order_confirmation.html', context)


@login_required(login_url='/login/')
def my_orders(request):
    """View user's orders"""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'my_orders.html', context)
