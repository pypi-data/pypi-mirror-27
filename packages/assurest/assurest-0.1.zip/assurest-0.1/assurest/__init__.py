import requests
import unittest

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
        return self.expected in value


class PreRequest:
    def __init__(self):
        self.header = {}

class TestCase:
    def __init__(self):
        self.pre_request = PreRequest()
        self.response = None
        self.request = None

    def headers(self, *params):
        #TODO: support dict
        if len(params)<1 or len(params)%2!=0:
            raise ValueError('Headers parameters must be even (name, value, ...)')
        for i in range(0,len(params)-1,2):
            self.pre_request.header[params[i]] = params[i+1]

    def header(self, name, value):
        self.headers(name, value)
        return self

    def perform_request(self, method, url):
        self.response = requests.request(method=method, url=url)
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

    def when(self):
        return self

    def then(self):
        if not self.response:
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
            raise AssertionError("Status '{actual}' didn't match {expected}".format(actual=actual_value, expected=str(matcher)))
        return self

def given():
    return TestCase()

class AssurestConfig():
    def __init__(self):
        self.follow_redirect = False
        self.base_url = None
