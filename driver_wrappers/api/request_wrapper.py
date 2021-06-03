import json
import requests
import pytest
import unittest
import urllib3
from factory.base_context import BaseContext as Bctx
from factory.handling.assertion import Assertion as Assert
from factory.handling.base_logging import BaseLogging as Log

from pactman import Consumer, Provider, Term, EachLike, Like, Includes

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.usefixtures("before_all")
class BaseRequests(Log):

    unittest.TestCase.maxDiff = None

    def __init__(self):
        super(BaseRequests, self).__init__()

    @staticmethod
    def assert_that(comparative_value=""):
        return Assert(comparative_value)

    @staticmethod
    def post(
        uri,
        path="",
        body_data="",
        json="",
        headers=None,
        auth=None,
        files=None,
        timeout=30,
        wait_status=200,
        **kwargs,
    ):
        response = requests.post(
            url=BaseRequests.__redress_endpoint(uri, path),
            data=body_data,
            json=json,
            headers=headers,
            auth=auth,
            files=files,
            timeout=timeout,
            **kwargs,
        )
        BaseRequests.assert_that(response.status_code).is_equals_to(
            wait_status, "[POST] Status Code"
        )
        return response

    @staticmethod
    def get(
        uri, path="", params=None, headers=None, auth=None, timeout=30, wait_status=200, **kwargs
    ):
        response = requests.get(
            url=BaseRequests.__redress_endpoint(uri, path),
            params=params,
            headers=headers,
            auth=auth,
            timeout=timeout,
            **kwargs,
        )
        BaseRequests.assert_that(response.status_code).is_equals_to(
            wait_status, "[GET] Status Code"
        )
        BaseRequests.show_response(response)
        return response

    @staticmethod
    def put(
        uri,
        path="",
        body_data="",
        json="",
        headers=None,
        auth=None,
        timeout=30,
        wait_status=200,
        **kwargs,
    ):
        response = requests.put(
            url=BaseRequests.__redress_endpoint(uri, path),
            data=body_data,
            json=json,
            headers=headers,
            auth=auth,
            timeout=timeout,
            **kwargs,
        )
        BaseRequests.assert_that(response.status_code).is_equals_to(
            wait_status, "[PUT] Status Code"
        )
        return response

    @staticmethod
    def delete(
        uri,
        path="",
        params=None,
        headers=None,
        auth=None,
        timeout=30,
        wait_status=200,
        **kwargs,
    ):
        response = requests.delete(
            url=BaseRequests.__redress_endpoint(uri, path),
            params=params,
            headers=headers,
            auth=auth,
            timeout=timeout,
            **kwargs,
        )
        BaseRequests.assert_that(response.status_code).is_equals_to(
            wait_status, "[DELETE] Status Code"
        )
        return response

    @staticmethod
    def response(response):
        return json.loads(response.text)

    @staticmethod
    def resp_decode(response):
        return response.content.decode()

    @staticmethod
    def resp_json(response):
        return response.json()

    @staticmethod
    def __redress_endpoint(uri, path):
        endpoint = f"{uri}{path}".split("://")
        endpoint_result = f'{endpoint[0]}://{endpoint[1].replace("//", "/")}'
        Log.info(endpoint_result)
        return endpoint_result
    
    @staticmethod
    def authenticate_api(email="", password=""):
        login_path = "/api/v1/default_login_path"
        request_body = {"email": email, "password": password}
        environment = Bctx.flag_environment.get()
        r = BaseRequests.post(
            uri=f"https://<THE_API_URL_>{environment}",
            path=login_path,
            body_data=request_body,
        )
        rdata = BaseRequests.resp_json(r)
        return rdata

    @staticmethod
    def pact(consumer="Consumer", provider="Provider"):
        return Consumer(consumer).has_pact_with(Provider(provider), version="3.0.0")


"""        
    headers_data: Pass to header your authentication data encoding to Base64 format your user/password in
                https://www.base64encode.org/ and use headers for authentication if you need it
                
            Samples:
            headers = { 'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_token)}
            headers = { 'Authorization' : 'Token ' + token }
            headers = { 'Authorization': 'Basic ' + encoded_pass }
            headers = { 'X-Api-Key': 'generated_api_key' }
"""