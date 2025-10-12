#!/usr/bin/env python
"""
Script to create a superuser for Render deployment.
Run this on Render after deployment.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entrack.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    username = 'admin'
    email = 'admin@entrack.com'
    password = 'admin123'  # Change this in production!
    
    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"✅ Superuser '{username}' created successfully!")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
        else:
            print(f"ℹ️  Superuser '{username}' already exists!")
            
        # Also create a regular test user
        test_username = 'testuser'
        if not User.objects.filter(username=test_username).exists():
            User.objects.create_user(username=test_username, email='test@entrack.com', password='test123')
            print(f"✅ Test user '{test_username}' created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating users: {e}")

if __name__ == '__main__':
    create_superuser()
