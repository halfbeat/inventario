"""Módulo de arranque de la aplicación Flask"""

import traceback
from flask import Flask, jsonify
from flask_restful import Api
from .ext import ma, migrate
from app.db import db
from app.common.error_handling import ObjectNotFound, AppErrorBaseClass
from app.authz.api_v1_0.resources import authz_v1_0_bp


def create_app(settings_module: str) -> Flask:
    """Create and configure an instance of the Flask application.

    Parámetros:
        settings_module: Módulo python con la configuración a utilizar"""

    app = Flask(__name__, instance_relative_config=True)
    # Carga los parámetros de configuración según el entorno
    app.config.from_object(settings_module)
    # Carga la configuración del directorio instance
    app.config.from_pyfile("config.py", silent=True)

    # Inicializa las extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Captura todos los errores 404
    Api(app, catch_all_404s=True)
    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False
    # Registra los blueprints
    app.register_blueprint(authz_v1_0_bp)

    # Registra manejadores de errores personalizados
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Registro de los manejadores de excepciones para devolver el contenido y erro HTTP de cada excepción"""

    @app.errorhandler(Exception)
    def handle_exception_error(e):
        print(traceback.format_exc())
        return jsonify({"msg": f"Internal server error: {e}"}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({"msg": "Method not allowed"}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({"msg": "Forbidden error"}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({"msg": "Not Found error"}), 404

    @app.errorhandler(409)
    def handle_409_error(e):
        return jsonify({"msg": "Conflict"}), 409

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({"msg": str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({"msg": str(e)}), 404
