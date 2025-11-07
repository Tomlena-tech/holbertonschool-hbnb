from app import create_app
from app.services import facade

app = create_app()

if __name__ == '__main__':
    # Créer automatiquement l'admin au démarrage
    with app.app_context():
        admin_email = 'admin@hbnb.com'
        existing_admin = facade.get_user_by_email(admin_email)
        
        if not existing_admin:
            admin_data = {
                'first_name': 'Admin',
                'last_name': 'User',
                'email': admin_email,
                'password': 'admin123',
                'is_admin': True
            }
            facade.create_user(admin_data)
            print("✅ Admin user auto-created: admin@hbnb.com / admin123")
        else:
            print("ℹ️  Admin user already exists")
    
    app.run(debug=True)
