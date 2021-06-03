from driver_wrappers.api.request_wrapper import BaseRequests
from pactman import Consumer, Provider, Term, EachLike, Like, Includes


uri_default = "https://swapi.dev"


class PactTest(BaseRequests):
    def test_get_swapi_planets(self):
        path = "/api/planets/14"
        expected = {
            "name": "Kashyyyk",
            "rotation_period": "26",
            "orbital_period": "381",
            "diameter": "12765",
            "climate": "tropical",
            "gravity": "1 standard",
            "terrain": "jungle, forests, lakes, rivers",
            "surface_water": "60",
            "population": "45000000",
            "residents": ["http://swapi.dev/api/people/13/", "http://swapi.dev/api/people/80/"],
            "films": ["http://swapi.dev/api/films/6/"],
            "created": "2014-12-10T13:32:00.124000Z",
            "edited": "2014-12-20T20:58:18.442000Z",
            "url": "http://swapi.dev/api/planets/14/",
        }
        (
            PactTest.pact()
            .given("a valid user and password to login into Gatekeeper")
            .upon_receiving("a user and password request")
            .with_request(
                method="GET",
                path=path,
            )
            .will_respond_with(
                200,
                body=expected,
            )
        )
        with PactTest.pact():
            r = self.get(uri=uri_default, path=path)
            rdata = PactTest.response(r)
        self.assert_that(self.response(r)).is_equals_to(expected, "Response Body - Planet Kashyyyk")
        return rdata