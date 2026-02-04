from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.views.decorators.http import require_POST
from main.models import Product, Category, Order, OrderItem, Cart
from userapp.models import UserProfile
import json
from datetime import datetime, timedelta

# Admin authentication decorator
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

# ============ PHASE 1: ADMIN DASHBOARD ============
@admin_required
def admin_dashboard(request):
    """Admin dashboard with key statistics"""
    
    # Calculate stats
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Recent orders (last 5)
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock__lt=5)
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    
    return render(request, 'adminapp/dashboard.html', context)

# ============ PHASE 2: VIEW USERS ============
@admin_required
def admin_users(request):
    """View all users with details"""
    
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(username__icontains=search_query) | users.filter(email__icontains=search_query)
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    
    return render(request, 'adminapp/users.html', context)

# ============ PHASE 2: ADD PRODUCT ============
@admin_required
def admin_add_product(request):
    """Add new product"""
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                name=name,
                category=category,
                price=price,
                description=description,
                stock=stock,
                image=image,
                is_active=True
            )
            return redirect('admin_products')
        except Exception as e:
            context = {
                'categories': categories,
                'error': str(e),
            }
            return render(request, 'adminapp/add_product.html', context)
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'adminapp/add_product.html', context)

# ============ PHASE 2: VIEW PRODUCTS ============
@admin_required
def admin_products(request):
    """View all products"""
    
    products = Product.objects.select_related('category').all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(category__name__icontains=search_query)
    
    context = {
        'products': products,
        'search_query': search_query,
    }
    
    return render(request, 'adminapp/products.html', context)

# ============ PHASE 3: VIEW ORDERS ============
@admin_required
def admin_orders(request):
    """View all orders"""
    
    orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Get status choices
    status_choices = Order._meta.get_field('status').choices
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': status_choices,
    }
    
    return render(request, 'adminapp/orders.html', context)

# ============ PHASE 3: UPDATE ORDER STATUS ============
@admin_required
@require_POST
def update_order_status(request, order_id):
    """Update order status"""
    
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order._meta.get_field('status').choices):
            order.status = new_status
            order.save()
    except:
        pass
    
    return redirect('admin_orders')

# ============ PHASE 3: SALES REPORT ============
@admin_required
def admin_reports(request):
    """Sales report with charts"""
    
    # Total stats
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = Order.objects.count()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Orders per day (last 7 days)
    today = datetime.now().date()
    last_7_days = []
    daily_orders = []
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Order.objects.filter(created_at__date=date).count()
        last_7_days.append(date.strftime('%a'))
        daily_orders.append(count)
    
    # Top products
    top_products = OrderItem.objects.values('product__name').annotate(
        total_qty=Sum('quantity')
    ).order_by('-total_qty')[:5]
    
    # Order status breakdown
    pending = Order.objects.filter(status='pending').count()
    confirmed = Order.objects.filter(status='confirmed').count()
    shipped = Order.objects.filter(status='shipped').count()
    delivered = Order.objects.filter(status='delivered').count()
    
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'last_7_days': json.dumps(last_7_days),
        'daily_orders': json.dumps(daily_orders),
        'top_products': top_products,
        'pending': pending,
        'confirmed': confirmed,
        'shipped': shipped,
        'delivered': delivered,
    }
    
    return render(request, 'adminapp/reports.html', context)
