"""
Manual review tests for Part 3 tasks.

Task 0: Validates that create_app() loads DevelopmentConfig by default
and that config values (DEBUG, SECRET_KEY) are accessible via app.config

Task 1: Validates that create_user() in facade hashes passwords
using Bcrypt before storing them.
"""
from app import create_app
from app.models.user import User

app = create_app()
# Task 0
print("---------------- 👀 Checking task 0 ---------------- \n")
print("Testing configuration loading...")
if app.config['DEBUG'] is True:
    print(f"✅ DEBUG value: {app.config['DEBUG']}")
else:
    print("❌ DEBUG is not set to True; check default config loading.")

if app.config['SECRET_KEY'] == 'default_secret_key':
    print(f"✅ SECRET_KEY value: {app.config['SECRET_KEY']}")
else:
    print("❌ SECRET_KEY is not set correctly; check default config loading.")


# Task 1
print("\n---------------- 👀 Checking task 1 ---------------- \n")
print("Testing password hashing in create_user()...")
with app.app_context():
    print("Creating a user with password...")
    user = User(
        first_name='jane',
        last_name='doe',
        email='jane.doe@example.com',
        password='MySecurePassword123!'


    )
    if user.password.startswith('$2b$'):
        print(f"✅ User created with hashed password: {user.password}")
    else:
        print("❌ Password hashing failed.")
