import json
from jinja2 import escape
from . import app


try:
    from urllib import urlencode as py_urlencode
except ImportError:
    from urllib.parse import urlencode as py_urlencode


@app.template_filter()
def urlencode(query):
    return py_urlencode(query) if query else ''


@app.template_filter()
def safe_json(json_):
    return escape(json.dumps(json_))
