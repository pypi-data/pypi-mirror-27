import requests
import unittest
import logging

# Helpers
def get_val_from_case_insensitive_key_in_dict(key, dict):
    for k in dict.keys():
        if key.lower() == k.lower():
            return dict.get(k)
    return None

# Matchers/ Comparators
class Matcher:
    def __init__(self, expected):
        self.expected = expected

    def __str__(self):
        return "{type} '{val}'".format(type=self.__class__.__name__, val=self.expected)

    def compare_to(self, value):
        return str(self.expected) == value

class equals(Matcher):
    def compare_to(self, value):
        return self.expected == value

class one_of(Matcher):
    def compare_to(self, value):
        for item in expected:
            if self.expected == value:
                return True
        return False

class contains(Matcher):
    def compare_to(self, value):
        return str(self.expected) in str(value)

class contains_one_of(Matcher):
    def compare_to(self, value):
        for item in expected:
            if str(self.expected) in str(value):
                return True
        return False


# Config for tests
class AssurestConfig:
    def __init__(self):
        self.request_follow_redirects = False
        self.default_base_url = None
        self.request_session = None
        self.logger = None

    def session(self, session):
        if not issubclass(session.__class__, requests.Session):
            raise ValueError('Invalid session type')
        self.request_session = session
        return self

    def follow_redirects(self, follow):
        self.request_follow_redirects = True if follow else False
        return self

    def redirects(self, follow): # just an alias
        return self.follow_redirects(follow)

    def base_url(self, url):
        self.default_base_url = url
        return self

    def logger(self, logger=None):
        self.logger = logger

def config():
    return AssurestConfig()

# Test itself
class AssurestTest:
    def __init__(self, config=None):
        self.response = None
        self.request = None
        self.config(config)
        self.pre_headers = {}
        self.pre_params = {}

    #Given
    def given(self): # not to be confused with the function given()
        if self.response:
            raise RuntimeError('Can\'t perform pre-request action after the request was performed')
        return self

    def config(self, test_config=None):
        if not test_config:
            self.configuration = config()
        else:
            if not issubclass(test_config.__class__, AssurestConfig):
                raise ValueError('Config provided is invalid (expected TestConfig class)')
            self.configuration = test_config
        return self

    def headers(self, *params):
        self.given()
        # if it is a dict
        if len(params) == 1 and isinstance(params[0], dict):
            for k, v in params[0].items():
                self.pre_headers[k] = v
            return self
        # if it is a even list of params
        if len(params)<1 or len(params)%2!=0:
            raise ValueError('Headers parameters must be even (name, value, ...)')
        for i in range(0,len(params)-1,2):
            self.pre_headers[params[i]] = params[i+1]
        return self

    def header(self, name, value):
        self.given()
        self.headers(name, value)
        return self

    def params(self, *params):
        self.given()
        # if it is a dict
        if len(params) == 1 and isinstance(params[0], dict):
            for k, v in params[0].items():
                self.pre_params[k] = v
            return self
        # if it is a even list of params
        if len(params)<1 or len(params)%2!=0:
            raise ValueError('Headers parameters must be even (name, value, ...)')
        for i in range(0,len(params)-1,2):
            self.pre_params[params[i]] = params[i+1]
        return self

    def log(self, type='all'):
        '''type can be one of the following:
            'all' (default) - gives you the full log
            'headers' - pre-requests headers or headers received (if request was performed)
            'body' - full response body (if request was performed)
            'config' - configuration prior to request
            'pre' - pre-request information (prior to request)
            'request' - request information
            'response' - response information'''
        def is_defined(setting):
            return (setting if isinstance(setting, str) else 'Defined') if setting else 'Undefined'
        log = self.configuration.logger.debug if self.configuration.logger else print
        request_performed = True if self.response else False
        if type == 'headers':
            if not request_performed:
                log('Pre-request Headers: {}'.format(self.pre_headers))
            else:
                log('Reponse Headers: {}'.format(self.response.headers))
        if type == 'body':
            log('Response Body: {}'.format(self.response.text if request_performed else 'Request not performed yet'))
        if type in ['all', 'config']:
            log('Configuration:')
            log('\tDefault Base-URL: {}'.format(is_defined(self.configuration.default_base_url)))
            log('\tDefault Session: {}'.format(is_defined(self.configuration.request_session)))
            log('\tFollow Redirects: {}'.format(self.configuration.request_follow_redirects))
            log('\tLogger: {}'.format(is_defined(self.configuration.logger)))
        if type in ['all', 'pre', 'config']:
            log('Pre-request:')
            log('\tHeaders: {}'.format(self.pre_headers))
            log('\tParameters: {}'.format(self.pre_params))
        if type in ['all', 'request']:
            log('Request:')
            if not request_performed:
                log('Request not yet performed')
            else:
                log('\tMethod: {}'.format(self.request.method))
                log('\tURL: {}'.format(self.request.url))
                log('\tHeaders: {}'.format(self.request.headers))
                log('\tBody: {}'.format(self.request.body))
        if type in ['all', 'response']:
            log('Response:')
            if not request_performed:
                log('Request not yet performed')
            else:
                log('\tStatus Code: {status} ({reason})'.format(status=self.response.status_code, reason=self.response.reason))
                log('\tIs Redirect: {}'.format(self.response.is_redirect))
                log('\tHeaders: {}'.format(self.response.headers))
                log('\tText (< 200 char): {}'.format(self.response.text[:200]))
        return self

    #When
    def when(self):
        return self.given()

    def perform_request(self, method, url):
        caller = requests.request if not self.configuration.request_session else self.configuration.request_session.request
        if self.configuration.default_base_url and not url.startswith('http'):
            url = self.configuration.default_base_url + url
        if self.pre_params:
            params_line = '&'.join(['{}={}'.format(k, v) for k, v in self.pre_params.items()])
            url = '{}{}{}'.format(url, '?' if '?' not in url else '&', params_line)
        self.response = caller(method=method, url=url, headers=self.pre_headers, allow_redirects=self.configuration.request_follow_redirects)
        self.request = self.response.request
        return self

    def get(self, url):
        return self.perform_request(method='get', url=url)

    def post(self, url):
        return self.perform_request(method='post', url=url)

    def put(self, url):
        return self.perform_request(method='put', url=url)

    def delete(self, url):
        return self.perform_request(method='delete', url=url)

    def options(self, url):
        return self.perform_request(method='options', url=url)

    def patch(self, url):
        return self.perform_request(method='patch', url=url)

    def head(self, url):
        return self.perform_request(method='head', url=url)

    def trace(self, url):
        return self.perform_request(method='trace', url=url)

    def then(self):
        if self.response == None:
            raise RuntimeError('No request to evaluate (you must perform a request first)')
        return self

    def assertThat(self):
        return self.then()

    def status(self, matcher):
        self.then()
        if not issubclass(matcher.__class__, Matcher):
            raise TypeError('Can only validate with a Matcher type (see matcher types)')
        actual_value = self.response.status_code
        if not matcher.compare_to(actual_value):
            raise AssertionError("Status '{actual}' did not match condition: {expected}".format(actual=actual_value, expected=str(matcher)))
        return self

    def body(self, matcher):
        self.then()
        '''if self._get_response_type() == 'application/json':
            body_to_compare = self.response.json()
        else: # xml not yet supported
            body_to_compare = self.response.text'''
        if not matcher.compare_to(self.response.text):
            raise AssertionError("Body did not match condition: {}".format(str(matcher)))
        return self

    '''def _get_response_type(self):
        if not self.response:
            return None
        type = get_val_from_case_insensitive_key_in_dict('content-type', self.response.headers)
        if 'application/json' in type.lower():
            return 'application/json'
        elif 'application/xml' in type.lower() or 'text/xml' in type.lower():
            'application/xml'
        return None'''

def given(config=None):
    return AssurestTest(config)
