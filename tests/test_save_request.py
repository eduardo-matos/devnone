from unittest import TestCase
import json
import re
from mock import patch
from datetime import datetime, tzinfo
from devnone.app import app
from . import create_redis, drop_redis


class RequestSavingTest(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.redis = create_redis()

    def tearDown(self):
        drop_redis(self.redis)

    def _get_result(self, response):
        key = json.loads(response.data)['_id']
        return self.redis.get(key)

    def test_response_must_be_json(self):
        resp = self.client.get('/api')
        self.assertEquals('application/json', resp.headers['Content-type'])

    def test_save_entry_in_redis_and_return_key_in_response(self):
        resp = self.client.get('/api')

        result = self._get_result(resp)
        self.assertNotEquals(None, result, 'result must contain content')

    def test_redis_key_must_be_uuid(self):
        resp = self.client.get('/api')
        data = json.loads(resp.data)

        self.assertTrue(re.match(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', data['_id']),
                        'redis key not in expected format')

    def test_save_get_params(self):
        resp = self.client.get('/api', data={'here': 'is', 'some': 'params'})
        self.assertEquals({'here': 'is', 'some': 'params'}, json.loads(self._get_result(resp))['GET'])

    def test_save_post_params(self):
        resp = self.client.post('/api', data={'ham': 'spam', 'wow': 'yay'})
        self.assertEquals({'ham': 'spam', 'wow': 'yay'}, json.loads(self._get_result(resp))['POST'])

    def test_save_get_and_post_params(self):
        resp = self.client.post('/api?ham=spam', data={'wow': 'yay'})
        self.assertEquals({'ham': 'spam'}, json.loads(self._get_result(resp))['GET'])
        self.assertEquals({'wow': 'yay'}, json.loads(self._get_result(resp))['POST'])

    def test_save_get_params_as_none_if_there_is_no_querystring_and_method_is_post(self):
        resp = self.client.post('/api', data={'blah': 'blah'})
        self.assertEquals(None, json.loads(self._get_result(resp))['GET'])

    def test_save_raw_body_content(self):
        resp = self.client.post('/api', data='body content')
        self.assertEquals('body content', json.loads(self._get_result(resp))['body'])

    def test_save_request_method(self):
        resp = self.client.post('/api')
        self.assertEquals('POST', json.loads(self._get_result(resp))['method'])

    def test_save_date_created(self):
        with patch('devnone.app.datetime') as appdatetime:
            appdatetime.utcnow.return_value = datetime(2017, 1, 3, 9, 11, 17)

            resp = self.client.get('/api')
            self.assertEquals('2017-01-03T09:11:17', json.loads(self._get_result(resp))['date_created'])
