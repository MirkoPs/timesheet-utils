from os import environ, path, getcwd

import tenacity
from dotenv import load_dotenv
from flask import Flask
from py_eureka_client import eureka_client


def get_db_path():
    return '{}+{}://{}:{}@{}:{}/{}'.format(
        environ.get('DB_DIALECT'),
        environ.get('DB_DRIVER'),
        environ.get('DB_USERNAME'),
        environ.get('DB_PASSWORD'),
        environ.get('DB_HOST'),
        environ.get('DB_PORT'),
        environ.get('DB_NAME')
    )


def get_eureka_path():
    return 'http://{}:{}/eureka/'.format(
        environ.get('EUREKA_HOST'),
        environ.get('EUREKA_PORT')
    )


class BaseConfig(object):
    basedir = path.abspath(getcwd())
    load_dotenv(path.join(basedir, '.env'))
    DATABASE_SERVER = get_db_path()

    EUREKA_SERVER = get_eureka_path()

    FLASK_RUN_PORT = environ.get('FLASK_RUN_PORT')


class TestConfig(object):
    TESTING = True


def create_app(bp, app_name, init_schema_func, config, tenacity_wait=30):
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config.from_object(config)

    @tenacity.retry(wait=tenacity.wait_fixed(tenacity_wait))
    def _init_service_discovery():
        eureka_client.init(eureka_server=config.EUREKA_SERVER,
                           app_name=app_name,
                           instance_port=config.FLASK_RUN_PORT)

    if not app.config['TESTING']:
        init_schema_func()
        _init_service_discovery()

    return app
