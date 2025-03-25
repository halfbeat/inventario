import os
from logging.config import dictConfig

from flask import request

from app import create_app

dictConfig({
    'version': 1,
    'root': {
        'level': 'DEBUG'
    }
})

settings_module = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings_module)


@app.before_request
def log_request():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Request body: %s', request.get_data())
