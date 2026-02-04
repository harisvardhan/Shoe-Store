from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Users
    path('users/', views.admin_users, name='admin_users'),
    
    # Products
    path('products/', views.admin_products, name='admin_products'),
    path('products/add/', views.admin_add_product, name='admin_add_product'),
    
    # Orders
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    
    # Reports
    path('reports/', views.admin_reports, name='admin_reports'),
]
