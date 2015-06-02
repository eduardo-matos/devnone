from jinja2 import escape
from devnone.models import Request, db
from . import BaseTest


class LatestRequestsTest(BaseTest):
    def test_show_latest_requests(self):
        db.session.add_all((Request(method='get', get={'yay': 'wow'}, body='building'),
                            Request(method='post', post={'ham': 'spam'}, body='shop'),))
        db.session.flush()

        resp = self.client.get('/requests').data.decode('utf-8')

        self.assertTrue(escape('{"yay": "wow"}') in resp, '\'{"yay": "wow"}\' not found in response')
        self.assertTrue(escape('{"ham": "spam"}') in resp, '\'{"ham": "spam"}\' not found in response')
        self.assertTrue('shop' in resp, '\'shop\' not found in response')
        self.assertTrue('building' in resp, '\'building\' not found in response')
        self.assertTrue('get' in resp, '\'get\' not found in response')
        self.assertTrue('post' in resp, '\'post\' not found in response')

    def test_limit_20_requests(self):
        for i in range(21):
            db.session.add(Request(method='get', body='building'))
        db.session.flush()

        resp = self.client.get('/requests').data.decode('utf-8')
        self.assertEquals(20, resp.count('building'))

    def test_show_message_if_there_are_no_requests(self):
        resp = self.client.get('/requests').data.decode('utf-8')
        self.assertTrue('Unbelievable! No requests so far!' in resp,
                        '\'Unbelievable! No requests so far!\' not found in response')
