from flask import Flask, jsonify
from flask_cors import CORS
from flask_request_validator.exceptions import InvalidRequest
from exceptions import InvalidUsage
from contextlib import suppress
from flask.json import JSONEncoder


app = Flask(__name__)

def create_app(test_config=None):

    def get_session():
        session = Session()
        return session

    app = Flask(__name__)

    CORS(app, resources={r'*': {'origins':'*'}})

    @app.errorhandler(Exception)
    def identify_invalid_usage(error):
        if isinstance(error, InvalidRequest) :
            return {'message': str(error)}, 400
        else:
            response = jsonify(error)
            response.status_code = error.status_code
            return response

    class MyJsonEncoder(JSONEncoder):
        def default(self,obj):
            with suppress(AttributeError) :
                return obj.isoformat()
            return dict(obj)

    app.json_encoder = MyJsonEncoder

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = ###############
    Sesion = sessionmaker(bind=database, autocommit=False)