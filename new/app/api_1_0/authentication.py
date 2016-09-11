from flask import g, jsonify
from .. models import User, AnonymousUser
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from . errors import unauthorized, forbidden
from . import api
from .control import request_wants_json

@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        #import pdb; pdb.set_trace()
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        #import pdb; pdb.set_trace()
        return g.current_user is not None
    #import pdb; pdb.set_trace()
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@api.before_request
@auth.login_required
def before_request():
    #import pdb; pdb.set_trace()
    if g.current_user.is_anonymous:
        if request_wants_json():
            return '{"code":403, "msg":"forbidden operation, please login first!"}'
        else:
            return 'forbidden operation', 403
    elif not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration':3600})


