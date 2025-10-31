from app import create_app
from app.services import facade

app = create_app()
with app.app_context():
    if not facade.get_user_by_email('admin@hbnb.com'):
        facade.create_user({
            'first_name':'Root',
            'last_name':'Admin',
            'email':'admin@hbnb.com',
            'password':'root123',
            'is_admin':True
        })
        print("✅ Admin créé : admin@hbnb.com / root123")
    else:
        print("ℹ️  Admin déjà présent")
