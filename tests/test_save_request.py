import json
import re
from devnone.app import app
from . import BaseTest
from devnone.models import Request, db


class RequestSavingTest(BaseTest):
    def _get_result(self, response):
        key = json.loads(response.data.decode('utf-8'))['_id']
        return db.session.query(Request).filter(Request.slug==key).first()

    def test_response_must_be_json(self):
        resp = self.client.get('/api')
        self.assertEquals('application/json', resp.headers['Content-type'])

    def test_save_entry_and_return_slug_in_response(self):
        resp = self.client.get('/api')

        result = self._get_result(resp)
        self.assertNotEquals(None, result, 'result must contain content')

    def test_slug_must_be_md5(self):
        resp = self.client.get('/api')
        data = json.loads(resp.data.decode('utf-8'))

        self.assertTrue(re.match(r'[a-f0-9]{32}', data['_id']), 'slug not in expected format')

    def test_save_get_params(self):
        resp = self.client.get('/api', data={'here': 'is', 'some': 'params'})
        self.assertEquals({'here': 'is', 'some': 'params'}, self._get_result(resp).get)

    def test_save_post_params(self):
        resp = self.client.post('/api', data={'ham': 'spam', 'wow': 'yay'})
        self.assertEquals({'ham': 'spam', 'wow': 'yay'}, self._get_result(resp).post)

    def test_save_get_and_post_params(self):
        resp = self.client.post('/api?ham=spam', data={'wow': 'yay'})
        self.assertEquals({'ham': 'spam'}, self._get_result(resp).get)
        self.assertEquals({'wow': 'yay'}, self._get_result(resp).post)

    def test_save_get_params_as_none_if_there_is_no_querystring_and_method_is_post(self):
        resp = self.client.post('/api', data={'blah': 'blah'})
        self.assertEquals(None, self._get_result(resp).get)

    def test_save_raw_body_content(self):
        resp = self.client.post('/api', data='body content')
        self.assertEquals('body content', self._get_result(resp).body)

    def test_save_request_method(self):
        resp = self.client.post('/api')
        self.assertEquals('POST', self._get_result(resp).method)
