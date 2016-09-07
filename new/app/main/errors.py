from flask import render_template, request, jsonify
from . import main


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@main.app_errorhandler(404)
def page_not_found(e):
    if request_wants_json():
        response = jsonify({'code': 404, 'msg': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    if request_wants_json():
        response = jsonify({'code': 500, 'msg': 'intenal error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
