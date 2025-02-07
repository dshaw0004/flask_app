import hashlib
from .fire import add_user, check_unique_username
from .fire import get_user_id

hasher = hashlib.new('sha256')

def sign_up(username: str, password: str) -> tuple[dict[str, str], int]:
    is_unique_name = check_unique_username(username=username)
    
    if not is_unique_name:
        return {'message': 'this username is already taken'}, 400
    hasher.update(password.encode()) 
    res = add_user(username=username, password=hasher.hexdigest())
    id = res.get('id', None)

    if not id:
        return {'message': 'sign up failed'}, 400

    return {'message': 'new user account created', 'id': id}, 200

def log_in(username: str, password: str) -> tuple[int, str]:
    hasher.update(password.encode()) 
    status_code, user_id = get_user_id(username=username, password=hasher.hexdigest())
    return status_code, user_id
