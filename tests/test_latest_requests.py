from datetime import datetime
from mock import patch
from jinja2 import escape
from devnone.app import app
from devnone.models import Request, db
from . import BaseTest


@patch.dict(app.config, {'BASE_URL': 'http://b.co'})
class LatestRequestsTest(BaseTest):
    def test_show_latest_requests(self):
        db.session.add_all((Request(method='get', get={'yay': 'wow'}, body='building',
                                    date_created=datetime(2003, 11, 15, 23, 4, 1)),
                            Request(method='post', post={'ham': 'spam'}, body='shop',
                                    date_created=datetime(2019, 2, 1, 9, 1, 17)),))
        db.session.flush()

        resp = self.client.get('/').data.decode('utf-8')

        self.assertTrue(escape('{"yay": "wow"}') in resp, '\'{"yay": "wow"}\' not found in response')
        self.assertTrue(escape('{"ham": "spam"}') in resp, '\'{"ham": "spam"}\' not found in response')
        self.assertTrue('shop' in resp, '\'shop\' not found in response')
        self.assertTrue('building' in resp, '\'building\' not found in response')
        self.assertTrue('get' in resp, '\'get\' not found in response')
        self.assertTrue('post' in resp, '\'post\' not found in response')
        self.assertTrue('2003-11-15 23:04:01' in resp, 'creation date not found in response')
        self.assertTrue('2019-02-01 09:01:17' in resp, 'creation date not found in response')

    def test_limit_20_requests(self):
        for i in range(21):
            db.session.add(Request(method='get', get={'wow': 'yep'}, slug='2280758ebd216238a9514c60e9a241db'))
        db.session.flush()

        resp = self.client.get('/').data.decode('utf-8')
        self.assertEquals(20, resp.count('/r/2280758ebd216238a9514c60e9a241db'))

    def test_show_message_if_there_are_no_requests(self):
        resp = self.client.get('/').data.decode('utf-8')
        self.assertTrue('Unbelievable! No requests so far!' in resp,
                        '\'Unbelievable! No requests so far!\' not found in response')

    def test_show_curl_options(self):
        db.session.add(Request(method='post', get={'yay': 'wow', 'pop': 'not'}, post={'ham': 'spam', 'sam': 'mam'},
                               body='building'))
        db.session.flush()

        resp = self.client.get('/').data.decode('utf-8')
        self.assertTrue(escape('curl -X POST http://b.co/r?yay=wow&pop=not --data "ham=spam&sam=mam"') in resp,
                        'curl not found in response')

    def test_dont_show_question_mark_in_curl_url_if_request_doesnt_have_get_params(self):
        db.session.add(Request(method='post', get=None, post={'ham': 'spam', 'sam': 'mam'}))
        db.session.flush()

        resp = self.client.get('/').data.decode('utf-8')
        self.assertTrue(escape('curl -X POST http://b.co/r --data "ham=spam&sam=mam"') in resp,
                        'curl not found in response')

    def test_show_request_body_in_curl_if_post_is_none_and_body_is_not_empty(self):
        db.session.add(Request(method='post', post=None, body='building'))
        db.session.flush()

        resp = self.client.get('/').data.decode('utf-8')
        self.assertTrue(escape('curl -X POST http://b.co/r --data "building"') in resp,
                        'curl not found in response')
