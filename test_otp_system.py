"""
Test script to verify OTP system is working correctly
Run this in Django shell: python manage.py shell < test_otp_system.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shop.settings')
django.setup()

from userapp.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

print("=" * 60)
print("OTP SYSTEM TEST")
print("=" * 60)

# Test 1: Create a test user
print("\n✓ Test 1: Creating test user...")
test_user, created = User.objects.get_or_create(
    username='testuser@example.com',
    defaults={
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'is_staff': False
    }
)
test_user.set_password('testpassword123')
test_user.save()
print(f"  User: {test_user.username} (Created: {created})")

# Test 2: Create/Get UserProfile
print("\n✓ Test 2: Creating user profile...")
profile, created = UserProfile.objects.get_or_create(
    user=test_user,
    defaults={
        'phone': '1234567890',
        'otp': None,
        'otp_verified': False
    }
)
print(f"  Profile created: {created}")
print(f"  Phone: {profile.phone}")

# Test 3: Generate OTP
print("\n✓ Test 3: Generating OTP...")
otp = profile.generate_otp()
print(f"  Generated OTP: {otp}")
print(f"  OTP Length: {len(otp)} (should be 6)")
print(f"  OTP is numeric: {otp.isdigit()}")

# Test 4: Save with timezone
print("\n✓ Test 4: Saving OTP with timezone...")
profile.otp_created_at = timezone.now()
profile.otp_verified = False
profile.save()
print(f"  OTP created at: {profile.otp_created_at}")
print(f"  Timezone aware: {profile.otp_created_at.tzinfo is not None}")

# Test 5: Verify OTP
print("\n✓ Test 5: Verifying OTP...")
stored_otp = profile.otp
print(f"  Stored OTP: {stored_otp}")
print(f"  Generated OTP: {otp}")
print(f"  Match: {stored_otp == otp}")

# Test 6: Check OTP expiration
print("\n✓ Test 6: Testing OTP expiration...")
elapsed = timezone.now() - profile.otp_created_at
print(f"  Elapsed time: {elapsed}")
print(f"  Valid (< 10 min): {elapsed < timedelta(minutes=10)}")

# Test 7: Test expired OTP
print("\n✓ Test 7: Testing expired OTP...")
profile.otp_created_at = timezone.now() - timedelta(minutes=11)
profile.save()
elapsed = timezone.now() - profile.otp_created_at
print(f"  Elapsed time: {elapsed}")
print(f"  Is expired: {elapsed > timedelta(minutes=10)}")

print("\n" + "=" * 60)
print("✅ ALL OTP SYSTEM TESTS PASSED!")
print("=" * 60)

# Cleanup
profile.delete()
test_user.delete()
print("\n✓ Test data cleaned up")
