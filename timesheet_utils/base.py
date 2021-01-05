import os

import tenacity
from flask import Flask
from py_eureka_client import eureka_client


def get_db_path():
    return '{}+{}://{}:{}@{}:{}/{}'.format(
        os.environ.get('DB_DIALECT'),
        os.environ.get('DB_DRIVER'),
        os.environ.get('DB_USERNAME'),
        os.environ.get('DB_PASSWORD'),
        os.environ.get('DB_HOST'),
        os.environ.get('DB_PORT'),
        os.environ.get('DB_NAME')
    )


def get_eureka_path():
    return 'http://{}:{}/eureka/'.format(
        os.environ.get('EUREKA_HOST'),
        os.environ.get('EUREKA_PORT')
    )


class BaseConfig(object):
    DATABASE_SERVER = get_db_path()
    EUREKA_SERVER = get_eureka_path()
    FLASK_RUN_PORT = int(os.environ.get('FLASK_RUN_PORT', '5000'))


def create_app(bp, app_name, init_schema_func, config=BaseConfig, tenacity_wait=30, prefix=''):
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix=prefix)
    app.config.from_object(config)
    app.url_map.strict_slashes = True
    print(config.DATABASE_SERVER)
    print(config.EUREKA_SERVER)
    @tenacity.retry(wait=tenacity.wait_fixed(tenacity_wait))
    def _init_service_discovery():
        print("eureka_client.init ...")
        eureka_client.init(eureka_server=config.EUREKA_SERVER,
                           app_name=app_name,
                           instance_port=config.FLASK_RUN_PORT)
    init_schema_func()
    _init_service_discovery()

    return app


def create_test_app(bp):
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config['TESTING'] = True

    return app
