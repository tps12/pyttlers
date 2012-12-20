from mock import MagicMock
from re import compile
from unittest import TestCase

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
from pyttlers.resources.base import Base

class StringMatching(object):
    def __init__(self, pattern):
        self.pattern = compile(pattern)

    def __eq__(self, other):
        if self.pattern.match(other):
            return True
        raise AssertionError, '{0} does not match {1}'.format(other, self.pattern.pattern)

class HeadersIncluding(object):
    def __init__(self, *expected):
        self.expected = expected

    def __eq__(self, other):
        for item in self.expected:
            try:
                k, v = item
            except ValueError:
                k, v = item, None
            for t in other:
                if t[0] == k:
                    if v is None or t[1] == v:
                        break
            else:
                raise AssertionError, 'No {0} found in {1}'.format(item, other)
        return True

class ResourceBaseTestCase(TestCase):
    start_response = MagicMock()
    
    class Resource(Base):
        url = '/some/resource/'
    Resource.methods = { 'GET': { }, 'POST': { } }

class Respond405(ResourceBaseTestCase):
    def setUp(self):
        self.env = { 'REQUEST_METHOD': 'PUT' }
        self.resource = self.Resource()

    def runTest(self):
        self.resource.respond(self.env, self.start_response)
        self.start_response.assert_called_with(StringMatching('^405'), HeadersIncluding(('Content-Type', 'text/plain')))
