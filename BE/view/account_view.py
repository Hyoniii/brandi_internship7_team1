from flask import request, Blueprint, jsonify, g
from datetime import datetime, timedelta
from flask.views import MethodView
from flask_request_validator import (
    GET,
    FORM,
    PATH,
    JSON,
    Param,
    Enum,
    Pattern,
    MinLength,
    MaxLength,
    validate_params
)
from service.account_service import AccountService
from db_connector import connect_db
from utils import login_validator


class AccountView:
    account_app = Blueprint('account_app', __name__, url_prefix='/account')

    @account_app.route('signup/master', methods=['POST'])
    @validate_params(
        Param('email', JSON, str,
              rules=[Pattern(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')]),
        Param('password', JSON, str,
              rules=[MaxLength(80), MinLength(4)]),
        Param('account_type_id', JSON, int),
        Param('account_type_id', JSON, str,
              rules=[Pattern(r"^[1-2]{1}$")]),
        Param('name', JSON, str, rules=[Pattern(r"^[가-힣]{1,20}$")]),
        Param('master_code', JSON, str, required=True)
    )
    def sign_up_master(*args):
        connection = None
        account_info = {
            'email': args[0],
            'password': args[1],
            'account_type_id': args[2],
            'name': args[4],
            'master_code': args[5]
        }

        connection = connect_db()
        if connection:
            account_service = AccountService()
            try:
                account_service.signup_account(account_info, connection)
                if account_info['master_code'] != 'brandi_team1':
                    connection.rollback()
                    return jsonify({'MESSAGE' : 'WRONG_MASTER_CODE'})
                connection.commit()
                connection.close()
                return jsonify({'MESSAGE': 'ACCOUNT_CREATED', }), 200
            except Exception as e:
                connection.rollback()
                return jsonify({'MESSAGE': f'{e}'}),400

    @account_app.route('signup/seller', methods=['POST'])
    @validate_params(
        Param('email', JSON, str,
              rules=[Pattern(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')]),
        Param('password', JSON, str, rules=[MaxLength(80), MinLength(4)]),
        Param('account_type_id', JSON, int),
        Param('account_type_id', JSON, str, rules=[Pattern(r"^[1-2]{1}$")]),
        Param('service_number', JSON, str, rules=[Pattern(r"^\d{3}-\d{3,4}-\d{4}$")]),
        Param('seller_name_kr', JSON, str, rules=[Pattern(r"^[가-힣]{1,20}$")]),
        Param('seller_name_en', JSON, str, rules=[Pattern(
            r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]{1,20}$")]),
        Param('subcategory_id', JSON, str, rules=[Pattern(r"^[1-8]{1}$")])
    )
    def sign_up_seller(*args):
        connection = None
        try:
            account_info = {
                'email': args[0],
                'password': args[1],
                'account_type_id': args[2],
                'name': '미설정',
                'service_number': args[4],
                'seller_name_kr': args[5],
                'seller_name_en': args[6],
                'subcategory_id': args[7],
                'seller_status_id': 1
            }

            connection = connect_db()
            account_service = AccountService()
            account_service.signup_seller(account_info, connection)
            connection.commit()

            return jsonify({'MESSAGE': 'SUCCESS'}), 200
        except Exception as e:
            connection.rollback()
            return jsonify({'MESSAGE': f'{e}'}), 500
        finally:
                connection.close()

    @account_app.route('/signin', methods=['POST'])
    def sign_in():
        connection = None
        try:
            connection = connect_db()
            login_data = request.json
            account_service = AccountService()
            token = account_service.signin(login_data, connection)
            return token
        except Exception as e:
            return jsonify ({'MESSAGE' : f'{e}'}, 400)

        finally:
            if connection:
                connection.close()


    @account_app.route('/seller_list', methods=['GET'])
    @login_validator
    @validate_params(
        Param('seller_id', GET, int, required=False),
        Param('account_id', GET, int, required=False),
        Param('email', GET, str, required=False),
        Param('seller_en', GET, str, required=False),
        Param('seller_kr', GET, str, required=False),
        Param('user_id', GET, int, required=False),
        Param('manager_name', GET, str, required=False),
        Param('manager_email', GET, str, required=False),
        Param('seller_status', GET, str, required=False),
        Param('manager_phone', GET, str, required=False),
        Param('seller_category', GET, str, required=False),
        Param('created_lower', GET, str, required=False),
        Param('created_upper', GET, str, required=False),
        Param('excel', GET, int, required=False),
        Param('offset', GET, int, required=False),
        Param('limit', GET, int, required=False),
        Param('order_by', GET, str, required=False, rules=[Enum('asc', 'desc')])
    )
    def list_sellers(*args):
        db_connection = None
        user = g.token_info
        filter_info = {
            'seller_id': args[0],
            'account_id': args[1],
            'email': args[2],
            'seller_en': args[3],
            'seller_kr': args[4],
            'user_id': args[5],
            'manager_name': args[6],
            'manager_email': args[7],
            'seller_status': args[8],
            'manager_phone': args[9],
            'seller_category': args[10],
            'created_upper': args[11],
            'created_lower': args[12],
            'excel': args[13],
            'offset': args[14] if args[14] else 0,
            'limit': args[15] if args[15] else 20,
            'order_by': args[16]
        }
        try:
            connection = connect_db()
            account_service = AccountService()
            seller_list = account_service.filter_seller(filter_info, user, connection)
            return jsonify({'seller_list': seller_list}), 200

        except Exception as e:
            return jsonify({'MESSAGE': f'{e}'}, 400)

        # except Exception as e:
        #     return jsonify({"message" : f'{e}'}), 400
        #
        # finally:
        #     if db_connection:
        #         db_connection.close()


    # @account_app.route('/password_change', methods=['POST'])
    # def change_password():
    #     try:
    #         brandiDB = connect_db()
    #         data = request.json
    #         return brandiDB
    #     except Exception as e:
    #         return jsonify ({'message' : f'{e}'}, 400)

    #     finally:
    #         if brandiDB:
    #             brandiDB.close()

    # def route_seller_endpoints(account_service):

    #     account_app = Blueprint('_', __name__, url_prefix='/account')

    #     @account_app.route('/signin', methods=['POST'])
    #     def signin():
    #         try:
    #             brandiDB = connect_db()
    #             data = request.json
    #             return brandiDB
    #         except Exception as e:
    #             return jsonify ({'message' : f'{e}'}, 400)

    #         finally:
    #             if brandiDB:
    #                 brandiDB.close()
