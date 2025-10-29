"""
Manual review tests for Part 3 tasks.

Task 0: Validates that create_app() loads DevelopmentConfig by default
and that config values (DEBUG, SECRET_KEY) are accessible via app.config
"""
from app import create_app

app = create_app()
# Task 0
print("---------------- 👀 Checking task 0 ---------------- \n")
print("Testing configuration loading...")
print(f"DEBUG value: {app.config['DEBUG']}")
print(f"SECRET_KEY value: {app.config['SECRET_KEY']}")
