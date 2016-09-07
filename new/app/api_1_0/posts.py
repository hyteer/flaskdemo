from flask import render_template, request, jsonify
from . import api


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@api.route('/test', methods=['GET','POST'])
def test():

    error = jsonify({'code':100, 'msg':'bad parameter'})

    if request.json:
        name = request.json.get('name')
        msg = jsonify({'code':0, 'msg': 'Hello {name}!'.format(name=name)})
        return msg
    elif request_wants_json():
        return error
    else:
        return "<h3>bad request</h3>"



