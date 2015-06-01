import json
from uuid import uuid4
from datetime import datetime
from devnone.app import app
from devnone.models import db, Request
from . import BaseTest


def _generate_uuid():
    return str()


class RetrieveRequestDataTest(BaseTest):
    def setUp(self):
        self.client = app.test_client()

    def test_response_is_json(self):
        slug = uuid4().hex
        db.session.add(Request(slug=slug, method='post'))
        db.session.commit()

        resp = self.client.get('/r/{0}'.format(slug))
        self.assertEquals('application/json', resp.headers['Content-type'])

    def test_return_full_response(self):
        slug = uuid4().hex
        now = datetime.utcnow()
        db.session.add(Request(slug=slug, get={'a': 1}, post={'b': 2}, body='c=3', method='post', date_created=now))
        db.session.commit()

        resp = self.client.get('/r/{0}'.format(slug))
        self.assertEquals({'GET': {'a': 1}, 'POST': {'b': 2}, 'body': 'c=3',
                           'date_created': now.isoformat(), 'method': 'post'},
                          json.loads(resp.data.decode('utf-8')))

    def test_return_404_if_data_doesnt_exist(self):
        resp = self.client.get('/r/abc')
        self.assertEquals(404, resp.status_code)
