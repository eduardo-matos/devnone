from unittest import TestCase
from devnone.app import app, db


def rebuild_schema():
    if 'sqlite' in db.engine.url.drivername:
        db.drop_all()
        db.create_all()
    else:
        raise Exception('dont date to test in {}!'.format(db.engine.url.drivername))


class BaseTest(TestCase):
    def __call__(self, *args, **kwargs):
        rebuild_schema()
        self.client = app.test_client()
        return super(BaseTest, self).__call__(*args, **kwargs)
