from app.utilities.decorators import page_not_found_404
from flask_restful import Resource


class BaseResource(Resource):
    """Base Resource class for all resources.

    Defines resource interface with a default of 404 for all routes.
    All routes not overridden will return a 404 - page not found.
    """

    @page_not_found_404
    def get(self):
        pass

    @page_not_found_404
    def post(self):
        pass

    @page_not_found_404
    def patch(self):
        pass

    @page_not_found_404
    def put(self):
        pass

    @page_not_found_404
    def delete(self):
        pass
