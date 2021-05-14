import os

from flask import Flask


def get_db_path():
    return os.path.expandvars(
        '{}+{}://{}:{}@{}:{}/{}'.format(
            os.environ.get('DB_DIALECT'),
            os.environ.get('DB_DRIVER'),
            os.environ.get('DB_USERNAME'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT'),
            os.environ.get('DB_NAME')
        )
    )


class BaseConfig(object):
    DATABASE_SERVER = get_db_path()
    FLASK_RUN_PORT = int(os.environ.get('FLASK_RUN_PORT', '5000'))


def create_app(bp, app_name, init_schema_func, config=BaseConfig, tenacity_wait=30, prefix=''):
    print("App init...")
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix=prefix)
    app.config.from_object(config)
    app.url_map.strict_slashes = True
    init_schema_func()
    print("App initialized!!!")
    return app


def create_test_app(bp):
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config['TESTING'] = True

    return app
