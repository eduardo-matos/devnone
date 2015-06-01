import os
from flask import Flask


app = Flask('devnone')

if os.environ.get('prod'):
    app.config.from_object('devnone.conf')
else:
    app.config.from_object('devnone.conf_dev')
