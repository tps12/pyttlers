from mock import MagicMock
from re import compile, match
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
        perform = MagicMock()

    Resource.methods = {
        'POST': [ { 'test/input.type': None }, None, { } ],
        'GET': [ { }, None, { 'test/output.type': None } ]
    }

class MethodNotAllowed(ResourceBaseTestCase):
    def setUp(self):
        self.env = { 'REQUEST_METHOD': 'PUT' }
        self.resource = self.Resource()

    def test_response(self):
        self.resource.respond(self.env, self.start_response)
        self.start_response.assert_called_with(StringMatching('^405'), HeadersIncluding(('Content-Type', 'text/plain')))

    def test_entity(self):
        text = self.resource.respond(self.env, self.start_response)[0]
        self.assertTrue(self.resource.url in text)
        self.assertTrue(all([m in text for m in self.resource.methods.keys()]))

class UnsupportedType(ResourceBaseTestCase):
    def setUp(self):
        self.env = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': 'some/unsupported.type',
            'CONTENT_LENGTH': 314
        }
        self.resource = self.Resource()

    def test_response(self):
        self.resource.respond(self.env, self.start_response)
        self.start_response.assert_called_with(StringMatching('^415'), HeadersIncluding(('Content-Type', 'text/plain')))

    def test_entity(self):
        text = self.resource.respond(self.env, self.start_response)[0]
        self.assertTrue(self.resource.url in text)
        self.assertTrue(all([t in text for t in self.resource.methods['POST'][0].keys()]))

class Unacceptable(ResourceBaseTestCase):
    def setUp(self):
        self.env = {
            'REQUEST_METHOD': 'GET',
            'HTTP_ACCEPT': 'some/unsupported.type'
        }
        self.resource = self.Resource()

    def test_response(self):
        self.resource.respond(self.env, self.start_response)
        self.start_response.assert_called_with(StringMatching('^406'), HeadersIncluding(('Content-Type', 'text/plain')))

    def test_entity(self):
        text = self.resource.respond(self.env, self.start_response)[0]
        self.assertTrue(self.resource.url in text)
        self.assertTrue(all([t in text for t in self.resource.methods['GET'][2].keys()]))

class UnexpectedEntity(ResourceBaseTestCase):
    def setUp(self):
        self.env = {
            'REQUEST_METHOD': 'GET',
            'CONTENT_TYPE': 'test/input.type',
            'CONTENT_LENGTH': 314,
            'HTTP_ACCEPT': 'test/output.type'
        }
        self.resource = self.Resource()

    def test_response(self):
        self.resource.respond(self.env, self.start_response)
        self.start_response.assert_called_with(StringMatching('^413'), HeadersIncluding(('Content-Type', 'text/plain')))

    def test_entity(self):
        text = self.resource.respond(self.env, self.start_response)[0]
        self.assertTrue(self.resource.url in text)

