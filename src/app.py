from apistar.backends.django_orm import components as django_components
from apistar.frameworks.wsgi import WSGIApp as App

from authentication.utils import TokenAuthentication
from config.settings import api_settings as django_settings
from config.routes import routes


app = App(
    routes=routes,
    settings={
        **django_settings,
        'AUTHENTICATION': [TokenAuthentication()],
    },
    components=django_components,
)


if __name__ == '__main__':
    app.main()
