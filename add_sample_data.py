import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shop.settings')
django.setup()

from main.models import Category, Product
from decimal import Decimal

# Clear existing data
Category.objects.all().delete()
Product.objects.all().delete()

# Create Categories
men_category = Category.objects.create(
    name="Men's Shoes",
    description="Premium collection of men's footwear"
)

women_category = Category.objects.create(
    name="Women's Shoes",
    description="Exclusive women's shoe collection"
)

unisex_category = Category.objects.create(
    name="Unisex Shoes",
    description="Comfortable shoes for everyone"
)

print("✅ Categories created!")

# Men's Shoes Products
men_products = [
    {
        "name": "Casual Running Shoes",
        "price": Decimal("7500.00"),
        "description": "Lightweight and comfortable running shoes perfect for daily activities",
        "stock": 50,
        "category": men_category
    },
    {
        "name": "Premium Formal Shoes",
        "price": Decimal("10800.00"),
        "description": "Elegant formal shoes ideal for business meetings and special occasions",
        "stock": 35,
        "category": men_category
    },
    {
        "name": "Sports Performance Shoes",
        "price": Decimal("10000.00"),
        "description": "High-performance athletic shoes designed for maximum comfort",
        "stock": 45,
        "category": men_category
    },
    {
        "name": "Urban Sneakers",
        "price": Decimal("8300.00"),
        "description": "Trendy urban sneakers with modern design and durability",
        "stock": 60,
        "category": men_category
    },
    {
        "name": "Classic Loafers",
        "price": Decimal("9150.00"),
        "description": "Timeless loafers perfect for casual and semi-formal occasions",
        "stock": 40,
        "category": men_category
    },
]

# Women's Shoes Products
women_products = [
    {
        "name": "Elegant Heels",
        "price": Decimal("8300.00"),
        "description": "Stylish high heels perfect for evening events and parties",
        "stock": 30,
        "category": women_category
    },
    {
        "name": "Comfortable Flats",
        "price": Decimal("6650.00"),
        "description": "Casual and comfortable flat shoes for everyday wear",
        "stock": 55,
        "category": women_category
    },
    {
        "name": "Women's Running Shoes",
        "price": Decimal("7900.00"),
        "description": "Lightweight running shoes designed specifically for women",
        "stock": 48,
        "category": women_category
    },
    {
        "name": "Trendy Boots",
        "price": Decimal("10000.00"),
        "description": "Fashionable boots perfect for any season",
        "stock": 35,
        "category": women_category
    },
    {
        "name": "Casual Sneakers",
        "price": Decimal("7500.00"),
        "description": "Cute and comfortable sneakers for casual outings",
        "stock": 50,
        "category": women_category
    },
]

# Unisex Shoes Products
unisex_products = [
    {
        "name": "Canvas Slip-Ons",
        "price": Decimal("5000.00"),
        "description": "Versatile canvas shoes perfect for casual occasions",
        "stock": 70,
        "category": unisex_category
    },
    {
        "name": "Minimalist Walking Shoes",
        "price": Decimal("6250.00"),
        "description": "Minimalist design with maximum comfort for all-day walking",
        "stock": 55,
        "category": unisex_category
    },
    {
        "name": "Adventure Hiking Boots",
        "price": Decimal("11650.00"),
        "description": "Durable hiking boots for outdoor adventures",
        "stock": 25,
        "category": unisex_category
    },
    {
        "name": "Casual Sandals",
        "price": Decimal("4150.00"),
        "description": "Comfortable sandals perfect for summer",
        "stock": 80,
        "category": unisex_category
    },
    {
        "name": "Professional Slides",
        "price": Decimal("5800.00"),
        "description": "Professional slides suitable for both home and casual outings",
        "stock": 60,
        "category": unisex_category
    },
]

# Add all products
all_products = men_products + women_products + unisex_products

for product_data in all_products:
    Product.objects.create(**product_data, is_active=True)

print(f"✅ {len(all_products)} products created!")
print("\n📊 Summary:")
print(f"   - Men's Shoes: {Product.objects.filter(category=men_category).count()}")
print(f"   - Women's Shoes: {Product.objects.filter(category=women_category).count()}")
print(f"   - Unisex Shoes: {Product.objects.filter(category=unisex_category).count()}")
print(f"   - Total Products: {Product.objects.count()}")
print(f"   - Total Categories: {Category.objects.count()}")
print("\n✨ Sample data added successfully!")
