"""This is a wrapper for a decorator that we can use on a request"""

import os
import traceback
from functools import wraps
from typing import Any, Callable

# Conditional Firebase imports to avoid issues when Firebase is not installed
try:
    import firebase_admin
    from firebase_admin import auth, credentials, firestore

    FIREBASE_AVAILABLE = True

    # Use a the given service account
    if os.path.exists("credentials.json"):
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred)
except ImportError:
    FIREBASE_AVAILABLE = False
    firebase_admin = None
    credentials = None
    firestore = None
    auth = None

from flask import abort, request


def check_auth(view_function: Callable[..., Any]) -> Callable[..., Any]:
    """This is used in the core app as part of a zero trust model to ensure users are
    authorized
    This would be part of a larger system where we also ensure
    only valid sources of queries can query the api in the first place
    (part of our cloud infrastructure)
    """

    @wraps(view_function)
    # This decorator allows us to globally call the function to check auth
    # regardless of source
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        """checks for verified request using firebase auth, this also gracefully handles
        anonymous user in the case of front ends where the user can't login"""
        # Check if Firebase is available
        if not FIREBASE_AVAILABLE:
            print("Firebase not available, skipping authentication")
            return view_function(*args, **kwargs)

        try:
            print("checking authorization...")
            headers = request.headers
            bearer = headers.get("Authorization")
            if not bearer:
                abort(401)

            token = bearer.split()[1]
            print("token", token)

            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]
            print("uid", uid)
            return view_function(*args, **kwargs)

        except Exception:
            print(traceback.format_exc())
            abort(401)

    return decorated_function
