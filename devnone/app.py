from flask import Flask, request, jsonify, abort, Response
from datetime import datetime
import json
import os
import redis
from uuid import uuid4


app = Flask('devnone')


if os.environ.get('prod'):
    app.config.from_object('devnone.conf')
else:
    app.config.from_object('devnone.conf_dev')


@app.route('/api', methods=['GET', 'POST'])
def api():
    redis_ = redis.StrictRedis(db=app.config['REDIS_DB'])
    key = str(uuid4())

    get_params = request.args if request.method == 'POST' else request.form

    redis_.set(key, json.dumps({'GET': get_params or None,
                                'POST': request.form or None,
                                'body': request.get_data(),
                                'method': request.method,
                                'date_created': datetime.utcnow().isoformat()}))

    return jsonify(_id=key)


@app.route('/r/<_id>', methods=['GET'])
def results(_id):
    redis_ = redis.StrictRedis(db=app.config['REDIS_DB'])
    result = redis_.get(_id)

    if result:
        return Response(result, content_type='application/json')

    return abort(404)


if __name__ == '__main__':
  app.run()
