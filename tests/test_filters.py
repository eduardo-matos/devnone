# coding: utf-8

from unittest import TestCase
from devnone.filters import urlencode, safe_json


class UrlencodeTest(TestCase):
    def test_encode_params(self):
        self.assertEquals(urlencode({'ham': ' josé'}), 'ham=+jos%C3%A9')

    def test_return_empty_string_if_query_is_none(self):
        self.assertEquals(urlencode(None), '')


class SafeJsonTest(TestCase):
    def test_return_unsafe_json(self):
        self.assertEquals(safe_json({'ham': 'john'}), '{&#34;ham&#34;: &#34;john&#34;}')
