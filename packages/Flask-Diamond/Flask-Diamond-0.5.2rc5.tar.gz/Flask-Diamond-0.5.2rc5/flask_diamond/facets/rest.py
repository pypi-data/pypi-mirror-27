# -*- coding: utf-8 -*-
# Flask-Diamond (c) Ian Dennis Miller

from flask_restful import Api

rest_api = Api()


def init_rest(self, api_map=None):
    """
    Initialize REST API.

    :returns: None

    By default, this function does nothing.  Your application needs to
    overload this function in order to implement your REST API.
    More information about REST can be found in the
    `documentation <http://flask-restful.readthedocs.org/en/latest/>`_.

    api_map is an optional function that can be responsible
    for setting up the API.  This is usually accomplished with a series of
    add_resource() invocations.  api_map must take one parameter, which is
    the Flask-Restful object managed by Flask-Diamond.

    You will end up writing something like this in your application:

    class PlanetResource(Resource):
        def get(self, name):
            planet = Planet.find(name=name)
            if planet:
                return(planet.dump())

    def api_map(rest_extension):
        rest_extension.add_resource(PlanetResource, '/api/planet/<string:name>')

    def create_app():
        application.facet("rest", api_map=api_map)
    """

    if api_map:
        api_map(rest_api)
    rest_api.init_app(self.app)
    return rest_api
