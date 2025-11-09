import os


class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

    # Admin user configuration
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@hbnb.io')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')
    ADMIN_FIRST_NAME = os.getenv('ADMIN_FIRST_NAME', 'Admin')
    ADMIN_LAST_NAME = os.getenv('ADMIN_LAST_NAME', 'HBnB')

    # Repository configuration
    REPOSITORY_TYPE = os.getenv('REPOSITORY_TYPE', 'in_memory')  # or 'database'

    # SQLAlchemy database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    @staticmethod
    def get_database_uri():
        """
        Construct database URI from environment variables.

        Environment Variables:
            DATABASE_URL: Complete database URL (takes precedence)
            DB_USER: Database username (default: hbnb_dev)
            DB_PASSWORD: Database password (default: hbnb_dev_pwd)
            DB_HOST: Database host (default: localhost)
            DB_NAME: Database name (default: hbnb_dev_db)

        Returns:
            str: SQLAlchemy database URI
        """
        # If DATABASE_URL is provided, use it directly
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            return database_url

        # Otherwise, construct from individual components
        # For MySQL/PostgreSQL, set DB_TYPE environment variable
        db_type = os.getenv('DB_TYPE', 'sqlite')
        db_name = os.getenv('DB_NAME', 'hbnb_dev_db')

        if db_type == 'sqlite':
            return f'sqlite:///{db_name}.db'

        # For other databases (MySQL, PostgreSQL)
        db_user = os.getenv('DB_USER', 'hbnb_dev')
        db_password = os.getenv('DB_PASSWORD', 'hbnb_dev_pwd')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306' if db_type == 'mysql' else '5432')

        return f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log SQL queries in development


class TestConfig(Config):
    """Test-specific configuration."""
    TESTING = True
    SQLALCHEMY_ECHO = False

    @staticmethod
    def get_database_uri():
        """Test database URI - uses in-memory SQLite."""
        return 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False

    @staticmethod
    def get_database_uri():
        """Production database URI - must be set via environment."""
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError(
                'DATABASE_URL environment variable must be set for production'
            )
        return database_url


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
