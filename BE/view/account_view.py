### OS ####
import requests
### FLASK ###
from flask import request, Blueprint, jsonify
from flask_request_validator import Param, PATH, GET, JSON
### USER ###
from db_connector import connect_db

def route_account_endpoints(account_service):

    account_app = Blueprint('account_app', __name__, url_prefix='/account')

    @account_app.route('/signin', methods=['POST'])
    def signin():
        try:
            brandiDB = connect_db()
            data = request.json
            return brandiDB
        except Exception as e:
            return jsonify ({'message' : f'{e}'}, 400)

        finally:
            if brandiDB:
                brandiDB.close()

    @account_app.route('/find', methods=['POST'])
    def get_user(*args):

        db_connection = None

        try:
            brandiDB = connect_db()
            data = request.json

            if brandi_DB:
                filter_info = {
                    'page'            : args[0],
                    'limit'           : args[1]
                }
        except Exception as e:
            return jsonify({"message" : f'{e}'}), 400

        finally:
            if db_connection:
                db_connection.close()

    @account_app.route('/signup', methods=['POST'])
    def signup():
        try:
            brandiDB = connect_db()
            data = request.json
            return brandiDB
        except Exception as e:
            return jsonify ({'message' : f'{e}'}, 400)

        finally:
            if brandiDB:
                brandiDB.close()

    @account_app.route('/navbar', methods=['GET'])
    def NavBar():
        try:
            brandiDB = connect_db()
            data = request.json
            return brandiDB ###different navbar items based on user 
        except Exception as e:
            return jsonify ({'message' : f'{e}'}, 400)

        finally:
            if brandiDB:
                brandiDB.close()

    @account_app.route('/password_change', methods=['POST'])
    def change_password():
        try:
            brandiDB = connect_db()
            data = request.json
            return brandiDB
        except Exception as e:
            return jsonify ({'message' : f'{e}'}, 400)

        finally:
            if brandiDB:
                brandiDB.close()

def route_seller_endpoints(account_service):

    account_app = Blueprint('_', __name__, url_prefix='/account')

    @account_app.route('/signin', methods=['POST'])
    def signin():
        try:
            brandiDB = connect_db()
            data = request.json
            return brandiDB
        except Exception as e:
            return jsonify ({'message' : f'{e}'}, 400)

        finally:
            if brandiDB:
                brandiDB.close()