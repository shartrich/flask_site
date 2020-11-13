from base64 import b64decode, b64encode
from utils.configs.settings import SERVER_USERNAME, SERVER_PASSWORD


def authenticate_request(request):
    headers = request.headers
    basic_auth = headers.get('Authorization', 'Basic X')
    auth_parts = b64decode(str.encode(basic_auth.split(' ')[1])).decode().split(':')
    print('auth_parts:', auth_parts)
    if auth_parts[0] == SERVER_USERNAME and auth_parts[1] == SERVER_PASSWORD:
        return True, {'user': auth_parts[0], 'success': True}
    return False, {'message': 'Invalid Authentication', 'success': False}
