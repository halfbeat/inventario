from functools import wraps
from flask import abort, jsonify, request
import jwt

from flask import current_app

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            abort(401, "Token is missing")
        try:
            pk = current_app.config["OAUTH2_PUBLIC_KEY"]
            parts = token.split(" ")
            if len(parts) != 2 or parts[0].upper() != "BEARER":
                abort(403, "Invalid token")
            jwt_token = jwt.decode(
                parts[1], pk, algorithms=["RS256"], options={"verify_aud": False}
            )            
        except Exception as e:
            abort(403, "Invalid token")
        kwargs["jwt_token"] = jwt_token
        return func(*args, **kwargs)

    return decorated
