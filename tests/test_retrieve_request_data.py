from unittest import TestCase
import json
from uuid import uuid4
from datetime import datetime, tzinfo
from devnone.app import app
from . import create_redis, drop_redis


def _generate_uuid():
    return str(uuid4())


class RetrieveRequestDataTest(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.redis = create_redis()

    def tearDown(self):
        drop_redis(self.redis)

    def test_response_is_json(self):
        _id = _generate_uuid()
        self.redis.set(_id, '{}')

        resp = self.client.get('/r/%s' % _id)
        self.assertEquals('application/json', resp.headers['Content-type'])

    def test_return_full_response(self):
        _id = _generate_uuid()
        self.redis.set(_id, '{"here": "I am"}')

        resp = self.client.get('/r/%s' % _id)
        self.assertEquals({'here': 'I am'}, json.loads(resp.data.decode('utf-8')))

    def test_return_404_if_data_doesnt_exist(self):
        resp = self.client.get('/r/abc')
        self.assertEquals(404, resp.status_code)
