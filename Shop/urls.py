"""
URL configuration for Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from main import views
from userapp import views as user_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('adminapp.urls')),
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('stock/', views.stock, name='stock'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    
    # User authentication URLs
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('verify-otp/', user_views.verify_otp, name='verify_otp'),
    path('logout/', user_views.logout_view, name='logout'),
    
    # Cart and Order URLs - PHASE 3
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
