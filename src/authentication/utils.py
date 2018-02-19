from apistar import http
from apistar.authentication import Authenticated
from apistar.backends.django_orm import Session


class TokenAuthentication():
    def authenticate(self, authorization: http.Header, session: Session):
        """
        Determine the user associated with a request based on a token sent over the Authorization
        header.
        """
        if authorization is None:
            return None

        scheme, token = authorization.split()
        if scheme.lower() != 'token':
            return None

        user_token = session.Token.objects.filter(key=token).first()
        if not user_token:
            return None

        return Authenticated(user_token.user.username, user=user_token.user)
