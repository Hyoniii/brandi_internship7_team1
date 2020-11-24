### OS ####
import requests
### FLASK ###
from flask import request, Blueprint, jsonify
from flask_request_validator import Param, PATH, GET, JSON
### USER ###
from db_connector import connect_db

def route_account(account_service):
    print('2')
    account_app = Blueprint('account_app', __name__, url_prefix='/account')
    print('3')
    @account_app.route('/signin', methods=['POST'])
    def signin():
        print('4')
        try:
            brandiDB = connect_db()
            print(brandiDB)
            data = request.json
            return brandiDB
        except Exception as e:
            return jsonify ({'message' : f'{e}'}, 400)

        finally:
            if brandiDB:
                brandiDB.close()


