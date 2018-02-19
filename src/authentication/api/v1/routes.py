from apistar import Response, Route, typesystem
from apistar.backends.django_orm import Session
from apistar.http import Response
from django.contrib.auth import authenticate


class AuthCredentials(typesystem.Object):
    properties = {
        'username': typesystem.string(max_length=50),
        'password': typesystem.string(max_length=50),
    }
    required = ('username', 'password',)


class Registration(AuthCredentials):
    properties = {
        **AuthCredentials.properties,
        'first_name': typesystem.string(max_length=50),
        'last_name': typesystem.string(max_length=50),
    }
    required = AuthCredentials.required + ('first_name', 'last_name')


class User(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'username': typesystem.string(max_length=50),
        'first_name': typesystem.string(max_length=50),
        'last_name': typesystem.string(max_length=50),
    }
    required = ('username', 'first_name', 'last_name')


class AuthResponse(typesystem.Object):
    properties = {
        'user': User,
        'token': typesystem.string(max_length=40)
    }


def login(session: Session, auth_credentials: AuthCredentials) -> AuthResponse:
    """
    Login user and exchange credentials for an API token.
    """
    user = authenticate(**auth_credentials)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=401)

    token, _ = session.Token.objects.get_or_create(user=user)

    return AuthResponse(user=user, token=token.key)


def register(session: Session, user_data: Registration) -> AuthResponse:
    """
    Create user with given credentials and authenticate them.
    """
    if session.User.objects.filter(username=user_data['username']).exists():
        return Response(status=400, content={
            'username': {
                'code': 'user_exists',
                'message': 'User with this username already exists',
            },
        })

    user = session.User.objects.create_user(**user_data)
    token = session.Token.objects.create(user=user)

    return AuthResponse(user=user, token=token.key)


routes = [
    Route('/login', 'POST', login, name='login'),
    Route('/register', 'POST', register, name='register'),
]
