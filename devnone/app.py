from flask import request, jsonify, abort, Response
from . import app
from .models import db, Request


@app.route('/api', methods=['GET', 'POST'])
def api():
    get_params = request.args if request.method == 'POST' else request.form

    user_request = Request(method=request.method, get=get_params or None, post=request.form or None,
                           body=request.get_data().decode('utf-8'))
    db.session.add(user_request)
    db.session.commit()

    return jsonify(_id=user_request.slug)


@app.route('/r/<slug>', methods=['GET'])
def results(slug):
    result = db.session.query(Request).filter(Request.slug == slug).first()

    if result:
        return Response(result.to_json(), content_type='application/json')

    return abort(404)


if __name__ == '__main__':
    app.run()
