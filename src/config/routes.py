from apistar import Include
from apistar.handlers import docs_urls, static_urls

from authentication.routes import routes as auth_routes


routes = [
    # Docs
    Include('/static', static_urls),
    Include('/api/docs', docs_urls),

    # APIs
    Include('/api/authentication', auth_routes, namespace='authentication'),
]
