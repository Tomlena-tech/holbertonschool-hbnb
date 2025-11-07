#!/usr/bin/env python3
"""
Script to create an admin user for testing Task 4
Run this script to create an admin user in your HBnB application
"""

from app import create_app
from app.services import facade

def create_admin_user():
    """Create an admin user with predefined credentials"""
    
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        # Admin user data
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@hbnb.com',
            'password': 'admin123',
            'is_admin': True  # This is the key part!
        }
        
        # Check if admin already exists
        existing_admin = facade.get_user_by_email(admin_data['email'])
        
        if existing_admin:
            print(f"❌ Admin user already exists with email: {admin_data['email']}")
            print(f"   User ID: {existing_admin.id}")
            print(f"   Is Admin: {existing_admin.is_admin}")
            return existing_admin
        
        # Create the admin user
        try:
            admin_user = facade.create_user(admin_data)
            print("✅ Admin user created successfully!")
            print(f"   Email: {admin_user.email}")
            print(f"   Password: admin123")
            print(f"   User ID: {admin_user.id}")
            print(f"   Is Admin: {admin_user.is_admin}")
            print("\n📝 You can now login with:")
            print(f"   Email: {admin_user.email}")
            print(f"   Password: admin123")
            return admin_user
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            return None

if __name__ == "__main__":
    print("=" * 50)
    print("Creating Admin User for HBnB Application")
    print("=" * 50)
    create_admin_user()
    print("=" * 50)
    