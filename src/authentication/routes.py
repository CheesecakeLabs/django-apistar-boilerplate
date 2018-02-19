from apistar import Include

from .api.v1.routes import routes as v1_routes


routes = [
    Include('/v1', v1_routes),
]
