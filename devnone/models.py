import json
from datetime import datetime
from uuid import uuid4
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import TypeDecorator, VARCHAR
from sqlalchemy.dialects import postgresql
from . import app


try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


db = SQLAlchemy(app)


class JSONType(TypeDecorator):
    impl = postgresql.JSON

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return self.impl
        else:
            return dialect.type_descriptor(VARCHAR)

    def process_bind_param(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        else:
            if value is not None:
                value = json.dumps(value)
            return value

    def process_result_value(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        else:
            if value is not None:
                value = json.loads(value)
            return value


class Request(db.Model):
    __table_name__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.Column(db.String(10), nullable=False)
    get = db.Column(JSONType)
    post = db.Column(JSONType)
    body = db.Column(db.String)
    slug = db.Column(db.String(32), default=lambda: uuid4().hex)

    def to_json(self):
        return json.dumps({'GET': self.get, 'POST': self.post, 'method': self.method, 'body': self.body,
                           'date_created': self.date_created.isoformat()})
