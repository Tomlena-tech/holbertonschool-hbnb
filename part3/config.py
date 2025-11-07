import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

    # Admin user configuration
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@hbnb.io')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')
    ADMIN_FIRST_NAME = os.getenv('ADMIN_FIRST_NAME', 'Admin')
    ADMIN_LAST_NAME = os.getenv('ADMIN_LAST_NAME', 'HBnB')


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
