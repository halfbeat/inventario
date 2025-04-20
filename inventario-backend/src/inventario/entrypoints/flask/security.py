from functools import wraps

import jwt
from flask import abort, request
from flask import current_app


def token_required(func):
    """
    Decorador Comprobación de que hay un token JWT y que confiamos en el
    :param func: función a la que llamar si la comprobacioón es correcta
    :return: el propio decorador
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        if current_app.config.get("NO_SECURITY", 0) == 1:
            return func(*args, **kwargs)
        else:
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
