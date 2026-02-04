from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage, get_connection
import logging
from django.conf import settings
from datetime import datetime, timedelta
from .models import UserProfile

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # Using email as username
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=name,
            password=password
        )
        
        # Create user profile
        UserProfile.objects.create(user=user, phone=phone)
        
        # Send welcome email
        subject = 'Welcome to Nexus Store!'
        welcome_message = f'''
Hi {name},

Welcome to Nexus Store! 🎉

We're thrilled to have you join our community of shoe enthusiasts. At Nexus Store, we're dedicated to bringing you the finest collection of premium shoes for every occasion.

**About Nexus Store:**
- Premium Quality Shoes: We carefully curate our collection to ensure only the best quality shoes make it to our store.
- Wide Variety: From running shoes to casual wear, formal shoes to sports gear - we have something for everyone.
- Best Prices: Enjoy competitive prices without compromising on quality.
- Fast Shipping: Free shipping on all orders with quick delivery times.
- Customer Support: Our dedicated team is here to help you 24/7.

**Your Account Details:**
- Email: {email}
- Phone: {phone}
- Name: {name}

**Next Steps:**
1. Log in to your account at https://nexusstore.com/login/
2. Browse our exclusive collections
3. Add items to your cart and checkout
4. Track your orders in real-time

**Special Offer:**
As a new member, you get **Flat 20% OFF** on your first purchase! Use any product code at checkout.

If you have any questions or need assistance, feel free to contact our support team at support@nexusstore.com or call us at +1-800-NEXUS-STORE.

Thank you for choosing Nexus Store. Happy shopping!

Best regards,
Nexus Store Team
        '''
        
        try:
            # Use explicit connection for clearer errors
            conn = get_connection(backend=settings.EMAIL_BACKEND, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
            email_msg = EmailMessage(subject=subject, body=welcome_message, from_email=settings.DEFAULT_FROM_EMAIL, to=[email], connection=conn)
            email_msg.content_subtype = 'plain'
            email_msg.send(fail_silently=False)
            messages.success(request, 'Account created successfully! Welcome email sent. Please login.')
        except Exception as e:
            logging.exception('Welcome email send failed')
            messages.success(request, 'Account created successfully! (Note: Welcome email could not be sent)')
        
        return redirect('login')
    
    return render(request, 'reg.html')


# Login View - Step 1: Send OTP
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if user exists
        try:
            user = User.objects.get(username=email)
            # Verify password
            user_auth = authenticate(request, username=email, password=password)
            
            if user_auth is not None:
                # Generate OTP
                profile = user.profile
                otp = profile.generate_otp()
                profile.otp_created_at = datetime.now()
                profile.otp_verified = False
                profile.save()
                
                # Send OTP via email
                subject = 'Your Nexus Store Login OTP'
                message = f'''
Hi {user.first_name},

Your OTP for Nexus Store login is: {otp}

This OTP is valid for 10 minutes.
If you didn't request this, please ignore this email.

Best regards,
Nexus Store Team
                '''
                
                try:
                    conn = get_connection(backend=settings.EMAIL_BACKEND, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
                    email_msg = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[email], connection=conn)
                    email_msg.content_subtype = 'plain'
                    email_msg.send(fail_silently=False)
                    # Store user ID in session for OTP verification
                    request.session['login_user_id'] = user.id
                    request.session['login_email'] = email
                    messages.success(request, 'OTP sent to your email! Please verify.')
                    return redirect('verify_otp')
                except Exception as e:
                    logging.exception('OTP send failed')
                    messages.error(request, f'Error sending OTP: {str(e)}')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid email or password!')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found! Please register first.')
            return redirect('register')
    
    return render(request, 'login.html')


# OTP Verification View - Step 2: Verify OTP
def verify_otp(request):
    if 'login_user_id' not in request.session:
        messages.error(request, 'Session expired! Please login again.')
        return redirect('login')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('login_user_id')
        
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            # Check OTP validity (10 minutes)
            if profile.otp_created_at:
                elapsed = datetime.now() - profile.otp_created_at.replace(tzinfo=None)
                if elapsed > timedelta(minutes=10):
                    messages.error(request, 'OTP expired! Please login again.')
                    del request.session['login_user_id']
                    del request.session['login_email']
                    return redirect('login')
            
            # Verify OTP
            if profile.otp == otp:
                profile.otp_verified = True
                profile.otp = None  # Clear OTP after verification
                profile.save()
                
                # Log user in
                login(request, user)
                
                # Clean session
                del request.session['login_user_id']
                del request.session['login_email']
                
                messages.success(request, f'Welcome {user.first_name}! Successfully logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP! Please try again.')
                return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'User not found!')
            return redirect('login')
    
    email = request.session.get('login_email', '')
    return render(request, 'verify_otp.html', {'email': email})


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


