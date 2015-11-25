import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask


app = Flask('devnone')

if os.environ.get('prod'):
    app.config.from_object('devnone.conf')
else:
    app.config.from_object('devnone.conf_dev')

# logging
handler = RotatingFileHandler(os.path.join(os.path.dirname(__file__), 'logs', 'devnone.log'), backupCount=10)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('{"%(levelname)s":"%(asctime)s", '
                                       '"%(funcName)s":%(lineno)d, "%(threadName)s":"%(message)s"}'))
app.logger.addHandler(handler)
