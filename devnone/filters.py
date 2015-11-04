import json
import urllib
from jinja2 import escape
from . import app


@app.template_filter()
def urlencode(query):
    return urllib.urlencode(query) if query else ''


@app.template_filter()
def safe_json(json_):
    return escape(json.dumps(json_))
