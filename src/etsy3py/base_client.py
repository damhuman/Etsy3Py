import requests
from requests.auth import HTTPBasicAuth
from requests import Request, Session


class BaseApiClient:
    base_url = "https://openapi.etsy.com"

    def __init__(self, token: str = None, client_id: str = None, token_type: str = None) -> None:
        self.__token_type = token_type
        self.__token = token
        self.__client_id = client_id
        self.session = Session()

    def _make_request(self,
                      path: str,
                      custom_base: str = None,
                      method: str = 'GET',
                      headers: dict = None,
                      data: dict = None,
                      params: dict = None,
                      auth_type: str = 'token') -> requests.Response:

        if not headers:
            headers = {}

        request_url = f"{custom_base if custom_base else self.base_url}{path}"

        auth = None
        if auth_type == 'basic':
            auth = HTTPBasicAuth(1, 1)
        if auth_type == 'token':
            headers['Authorization'] = f'{self.__token_type} {self.__token}'
            headers['x-api-key'] = f'{self.__client_id}'

        request = Request(method=method,
                          url=request_url,
                          headers=headers,
                          data=data,
                          params=params,
                          auth=auth).prepare()
        response = self.session.send(request)
        return response

    def _post(self, path: str, data: dict = None, headers: dict = None,
              auth_type: str = 'none') -> requests.Response:
        return self._make_request(path=path, method='POST', data=data,
                                  headers=headers, auth_type=auth_type)

    def _get(self, path: str, params: dict = None, headers: dict = None,
             auth_type: str = 'none') -> requests.Response:
        return self._make_request(path=path, method='GET', params=params,
                                  headers=headers, auth_type=auth_type)

    def _patch(self, path: str, data: dict = None, headers: dict = None,
               auth_type: str = 'none') -> requests.Response:
        return self._make_request(path=path, method='PATCH', data=data,
                                  headers=headers, auth_type=auth_type)

    def _put(self, path: str, data: dict = None, headers: dict = None,
             auth_type: str = 'none') -> requests.Response:
        return self._make_request(path=path, method='PUT', data=data,
                                  headers=headers, auth_type=auth_type)

    def _delete(self, path: str, params: dict = None, headers: dict = None,
                auth_type: str = 'none') -> requests.Response:
        return self._make_request(path=path, method='DELETE', params=params,
                                  headers=headers, auth_type=auth_type)
