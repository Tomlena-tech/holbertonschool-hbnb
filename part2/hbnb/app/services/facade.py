"""Minimal facade pour faire tourner le namespace users avec TES modèles"""
from models.user import User

# stockage volatile
_USERS = {}      # uuid -> User instance


# ------- helpers -------
def _to_dict(user):
    """Extract public fields from YOUR User class"""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


# ------- API methods -------
def get_all_users():
    return list(_USERS.values())


def get_user_by_email(email):
    for u in _USERS.values():
        if u.email == email:
            return u
    return None


def get_user(user_id):
    return _USERS.get(user_id)


def create_user(data):
    """data = {'first_name': ..., 'last_name': ..., 'email': ...}"""
    try:
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
    except (TypeError, ValueError) as exc:
        # flask-restx renverra automatiquement 400
        raise ValueError(str(exc))
    _USERS[user.id] = user
    return user


def update_user(user_id, data):
    user = _USERS.get(user_id)
    if not user:
        return None
    # On utilise TON setter (validation incluse)
    for key in ('first_name', 'last_name', 'email'):
        if key in data:
            setattr(user, key, data[key])
    user.save()          # BaseModel
    return user
