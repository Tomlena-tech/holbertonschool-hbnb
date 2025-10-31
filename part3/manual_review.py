"""
Manual review tests for Part 3 tasks.

Task 0: Validates that create_app() loads DevelopmentConfig by default
and that config values (DEBUG, SECRET_KEY) are accessible via app.config

Task 1: Validates that create_user() in facade hashes passwords
using Bcrypt before storing them.

Task 2: Validates that the /api/v1/auth/login endpoint correctly
authenticates a user and returns a JWT token, and that a protected
endpoint can be accessed with the token.
"""
from app import create_app
from app.models.user import User

app = create_app()

# Task 0:
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


# Task 1:
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


# Task 2:
print("\n---------------- 👀 Checking task 2 ---------------- \n")
print("Testing JWT authentication...")

with app.app_context():
    from app.services import facade

    # Create a user to test login (using facade to persist it)
    user = facade.create_user({
        'first_name': 'john',
        'last_name': 'doe',
        'email': 'john.doe@example.com',
        'password': 'Password123!'
    })

    with app.test_client() as client:
        res = client.post('/api/v1/auth/login', json={
            'email': 'john.doe@example.com',
            'password': 'Password123!'
        })

        data = res.get_json()
        if res.status_code == 200 and 'access_token' in data:
            print(f"✅ Login successful, received JWT token: {data['access_token']}")
            token = data['access_token']
            headers = {
                'Authorization': f'Bearer {token}'
            }
            protected_res = client.get('/api/v1/auth/protected', headers=headers)
            protected_data = protected_res.get_json()
            if (protected_res.status_code == 200
                    and 'message' in protected_data
                    and str(user.id) in str(protected_data.get('message'))):
                msg = protected_data.get('message')
                print("✅ Protected route accessed successfully:", msg)
            else:
                print(f"❌ Failed to access protected route. Status: {protected_res.status_code}, Data: {protected_data}")
        else:
            print(f"❌ Login failed. Status: {res.status_code}, Data: {data}")