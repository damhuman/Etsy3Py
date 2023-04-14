from requests.auth import HTTPBasicAuth
from requests import Request, Session
 
 
class BaseApiClient:
    base_url = "https://openapi.etsy.com"
    __token_type = None
    __token = None
    __token_expire = None
    session = Session()
 
    def _make_request(self,
                      path: str,
                      custom_base: str = None,
                      method: str = 'GET',
                      headers: dict = None,
                      data: dict = None,
                      params: dict = None,
                      auth_type: str = 'token'):
        if auth_type == 'token':
            self.check_token()
        if not headers:
            headers = {}
 
        request_url = f"{custom_base if custom_base else self.base_url}{path}"
 
        auth = None
        if auth_type == 'basic':
            auth = HTTPBasicAuth(1, 1)
        if auth_type == 'token':
            headers['Authorization'] = f'{self.__token_type} {self.__token}'
 
        request = Request(method=method,
                          url=request_url,
                          headers=headers,
                          data=data,
                          params=params,
                          auth=auth).prepare()
        response = self.session.send(request)
        return response
 
    def _post(self, path: str, data: dict = None, headers: dict = None, auth_type: str = 'none'):
        return self._make_request(path=path, method='POST', data=data,
                                  headers=headers, auth_type=auth_type)
 
    def _get(self, path: str, params: dict = None, headers: dict = None, auth_type: str = 'none'):
        return self._make_request(path=path, method='GET', params=params,
                                  headers=headers, auth_type=auth_type)

    def _put(self, path: str, params: dict = None, headers: dict = None, auth_type: str = 'none'):
        return self._make_request(path=path, method='PUT', params=params,
                                  headers=headers, auth_type=auth_type)

    def _delete(self, path: str, params: dict = None, headers: dict = None, auth_type: str = 'none'):
        return self._make_request(path=path, method='DELETE', params=params,
                                  headers=headers, auth_type=auth_type)
