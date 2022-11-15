"""This is a wrapper for a decorator that we can use on a request"""
from functools import wraps

from flask import abort, current_app, request

def check_auth(view_function):
    """This is used in the core app as part of a zero trust model to ensure users are authorized
    This would be part of a larger system where we also ensure
    only valid users can query the api in the first place (part of our cloud infrastructure)"""
    @wraps(view_function)
    #This decorator allows us to globally call the function to check auth regardless of source
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get(
                'x-api-key') == current_app.config['API_KEY']:
            return view_function(*args, **kwargs)
        
        abort(401)
    return decorated_function
