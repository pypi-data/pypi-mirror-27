from requests.auth import HTTPBasicAuth
import requests
import time
from functools import partial


class OrthancRestApiException(Exception):

    def __init__(self, msg = "Unknown Orthanc Rest API exception", url = None):
        self.msg = msg
        self.url = url

    def __str__(self):
        return "Orthanc API exception: '{msg}' while accessing '{url}'".format(msg = self.msg, url = self.url)


class ConnectionError(OrthancRestApiException):
    def __init__(self, msg = "Could not connect to Orthanc.", url = None):
        super(ConnectionError, self).__init__(msg = msg, url = url)

class TimeoutError(OrthancRestApiException):
    def __init__(self, msg = "Timeout.  Orthanc took too long to respond.", url = None):
        super(TimeoutError, self).__init__(msg = msg, url = url)

class HttpError(OrthancRestApiException):

    def __init__(self, httpStatusCode = None, msg = "Unknown Orthanc HTTP Rest API exception", url = None, requestResponse = None):
        super(HttpError, self).__init__(msg = msg, url = url)
        self.httpStatusCode = httpStatusCode
        self.requestResponse = requestResponse

    def __str__(self):
        return "Orthanc HTTP API exception: '{httpStatusCode} - {msg}' while accessing '{url}'".format(httpStatusCode = self.httpStatusCode, msg = self.msg, url = self.url)


class ResourceNotFound(HttpError):
    def __init__(self, msg = "Resource not found.  The resource you're trying to access does not exist in Orthanc.", url = None):
        super(ResourceNotFound, self).__init__(httpStatusCode = 404, msg = msg, url = url)

class NotAuthorized(HttpError):
    def __init__(self, httpStatusCode, msg = "Not authorized.  Make sure to provide login/pwd.", url = None):
        super(NotAuthorized, self).__init__(httpStatusCode = httpStatusCode, msg = msg, url = url)




class OrthancMinimalHttpClient:

    def __init__(self, rootUrl = 'http://127.0.0.1:8042', userName = None, password = None, logger = None, caFile = None, headers = {}, numConnections = None, httpProxy = None, httpsProxy = None):
        self._rootUrl = rootUrl
        self._httpSession = requests.Session()

        self._httpSession.headers.update(headers)

        if userName is not None and password is not None:
            self._httpSession.auth = HTTPBasicAuth(userName, password)

        if caFile is not None:
            self._httpSession.verify = caFile

        self._logger = logger
        self._retriesCount = 3
        self._retriesDelay = 1

        if numConnections is not None:
            adapter = requests.adapters.HTTPAdapter(pool_maxsize = numConnections)
            self._httpSession.mount('http://', adapter)
            self._httpSession.mount('https://', adapter)

        if httpProxy is not None or httpsProxy is not None:
            proxies = {}
            if httpProxy is not None:
                proxies['http'] = httpProxy
            if httpsProxy is not None:
                proxies['https'] = httpsProxy

            self._httpSession.proxies = proxies

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._httpSession.close()

    def setRetryPolicy(self, retries, delay):
        """ change the default values for retries/delay"""
        self._retriesCount = retries
        self._retriesDelay = delay

    def _retry(self, partial):
        """ internal call to retry one of the _get/_post/.. call"""
        if 'delay' in partial.keywords:
            delay = partial.keywords['delay']
            del partial.keywords['delay']
        else:
            delay = self._retriesDelay
        if 'retries' in partial.keywords:
            retries = partial.keywords['retries']
            del partial.keywords['retries']
        else:
            retries = self._retriesCount

        retryCount = 0
        while True:
            try:
                return partial()
            except ConnectionError as ex:
                if retryCount < retries:
                    retryCount += 1
                    print('retrying')
                    time.sleep(delay)
                else:
                    raise ex

    def _getAbsoluteUrl(self, relativeUrl):
        if relativeUrl is None:
            return self._rootUrl

        if self._rootUrl.endswith('/'):
            if not relativeUrl.startswith('/'):
                return self._rootUrl + relativeUrl
            else:
                return self._rootUrl + relativeUrl[1:]
        else:
            if not relativeUrl.startswith('/'):
                return self._rootUrl + '/' + relativeUrl
            else:
                return self._rootUrl + relativeUrl

    def get(self, relativeUrl, params = None, **kwargs):
        functionCall = partial(self._get, relativeUrl, params, **kwargs)
        return self._retry(functionCall)

    def _get(self, relativeUrl, params = None, **kwargs):
        absoluteUrl = self._getAbsoluteUrl(relativeUrl = relativeUrl)
        try:
            response = self._httpSession.get(
                url = absoluteUrl,
                params = params,
                **kwargs
            )
        except requests.RequestException as requestException:
            self._translateException(requestException, url = absoluteUrl)

        self._raiseOnErrors(response, url = absoluteUrl)
        return response

    def getJson(self, relativeUrl, params = None, **kwargs):
        response = self.get(
            relativeUrl = relativeUrl,
            params = params,
            **kwargs
        )

        return response.json()

    def post(self, relativeUrl, **kwargs):
        functionCall = partial(self._post, relativeUrl, **kwargs)
        return self._retry(functionCall)   # note: it might not be wise to retry POST requests since they might not be idempotent https://bitbucket.org/osimis/pythontoolbox/commits/4645273116830cbc8dd09e4c9cb4c0783508f8ca#comment-5038524

    def _post(self, relativeUrl, **kwargs):
        absoluteUrl = self._getAbsoluteUrl(relativeUrl = relativeUrl)
        try:
            response = self._httpSession.post(
                url = absoluteUrl,
                **kwargs
            )
        except requests.RequestException as requestException:
            self._translateException(requestException, url = absoluteUrl)

        self._raiseOnErrors(response, url = absoluteUrl)
        return response

    def put(self, relativeUrl, **kwargs):
        functionCall = partial(self._put, relativeUrl, **kwargs)
        return self._retry(functionCall)

    def _put(self, relativeUrl, **kwargs):
        absoluteUrl = self._getAbsoluteUrl(relativeUrl = relativeUrl)
        try:
            response = self._httpSession.put(
                url = absoluteUrl,
                **kwargs
            )
        except requests.RequestException as requestException:
            self._translateException(requestException, url = absoluteUrl)

        self._raiseOnErrors(response, url = absoluteUrl)
        return response

    def delete(self, relativeUrl, **kwargs):
        functionCall = partial(self._delete, relativeUrl, **kwargs)
        return self._retry(functionCall)

    def _delete(self, relativeUrl, raiseOnErrors = True, **kwargs):
        absoluteUrl = self._getAbsoluteUrl(relativeUrl = relativeUrl)

        try:
            response = self._httpSession.delete(
                    url = absoluteUrl,
                    **kwargs
                )
        except requests.RequestException as requestException:
            self._translateException(requestException, url = absoluteUrl)

        if raiseOnErrors:
            self._raiseOnErrors(response, url = absoluteUrl)
        return response

    def _raiseOnErrors(self, response, url):
        if response.status_code == 200:
            return

        if response.status_code == 401:
            raise NotAuthorized(response.status_code, url = url)
        elif response.status_code == 404:
            raise ResourceNotFound(response.status_code, url = url)
        else:
            raise HttpError(response.status_code, url = url, requestResponse = response)

    def _translateException(self, requestException, url):
        if isinstance(requestException, requests.ConnectionError):
            raise ConnectionError(url = url)
        elif isinstance(requestException, requests.Timeout):
            raise TimeoutError(url = url)

    def isAlive(self):
        """
        checks if the orthanc server can be reached.
        Returns:
            True if orthanc can be reached, False otherwise
        """
        try:
            # if we get an answer to a basic request, it means the server is alive
            self.get('system', retries = 0, timeout = 0.1)
            return True
        except ConnectionError:
            return False
        except TimeoutError:
            return False
