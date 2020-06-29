import os

import tenacity
from flask import Flask
from py_eureka_client import eureka_client


def create_app(bp, eureka_path, app_name, init_schema_func, tenacity_wait=30):
    app = Flask(__name__)
    app.register_blueprint(bp)

    @tenacity.retry(wait=tenacity.wait_fixed(tenacity_wait))
    def _init_service_discovery():
        eureka_client.init(eureka_server=eureka_path,
                           app_name=app_name,
                           instance_port=int(os.getenv('FLASK_RUN_PORT')))

    @app.before_first_request
    def _init():
        if not app.config['TESTING']:
            init_schema_func()
            _init_service_discovery()

    return app
