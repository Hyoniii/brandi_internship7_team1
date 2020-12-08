from flask import request, Blueprint, jsonify, g
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
                return jsonify({'MESSAGE': f'{e}'}), 400
            finally:
                connection.close()

    @account_app.route('signup/seller', methods=['POST'])
    @validate_params(
        Param('email', JSON, str,
              rules=[Pattern(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')]),
        Param('password', JSON, str, rules=[MaxLength(80), MinLength(4)]),
        Param('account_type_id', JSON, int),
        Param('account_type_id', JSON, str, rules=[Pattern(r"^[1-2]{1}$")]),
        Param('service_number', JSON, str, rules=[Pattern(r"^[0-9]{11}$|^[0-9]{12}$")]),
        Param('seller_name_kr', JSON, str, rules=[Pattern(r"^[가-힣0-9]{1,20}$")]),
        Param('seller_name_en', JSON, str, rules=[Pattern(
            r"^[a-zA-Z0-9àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]{1,20}$")]),
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
            return jsonify ({'MESSAGE' : f'{e}'}), 400
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
        Param('page', GET, int, required=False),
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
            'page': args[14] if args[14] else 1,
            'limit': args[15] if args[15] else 10,
            'order_by': args[16]
        }
        try:
            connection = connect_db()
            account_service = AccountService()
            seller_list = account_service.filter_seller(filter_info, user, connection)
            return jsonify({'seller_list': seller_list}), 200

        except Exception as e:
            return jsonify({'MESSAGE': f'{e}'}), 400
        finally:
            connection.close()

    @account_app.route('edit', methods=['PATCH'])
    @login_validator
    @validate_params(
        Param('email', JSON, str,
              rules=[Pattern(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')], required=False),
        Param('password', JSON, str,
              rules=[MaxLength(80), MinLength(4)], required=False),
        Param('account_type_id', JSON, int, required=False),
        Param('account_type_id', JSON, str,
              rules=[Pattern(r"^[1-2]{1}$")], required=False),
        Param('name', JSON, str, rules=[Pattern(r"^[가-힣]{1,20}$")], required=False),
        Param('account_id', JSON, int, required=True),
        Param('is_active', JSON, int, required=False)
    )
    def edit_account(*args):
        connection = None
        change_info = {
            'email': args[0],
            'password': args[1],
            'account_type_id': args[2],
            'name': args[4],
            'id': args[5],
            'is_active': args[6]
        }

        connection = connect_db()
        user = g.token_info
        if connection:
            account_service = AccountService()
            try:
                change_account = account_service.change_account_info(change_info, user, connection)
                connection.commit()
                return change_account
            except Exception as e:
                connection.rollback()
                return jsonify({'MESSAGE': f'{e}'}), 400
            finally:
                connection.close()

    @account_app.route('edit_seller', methods=['PATCH'])
    @login_validator
    @validate_params(
        Param('subcategory_id', JSON, int, required= False),
        Param('seller_status_id', JSON, int, required= False),
        Param('seller_name_kr', JSON, str, rules=[Pattern(r"^[가-힣0-9]{1,20}$")], required= False),
        Param('seller_name_en', JSON, str, rules=[Pattern(
            r"^[a-zA-Z0-9àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]{1,20}$")], required= False),
        Param('seller_number', JSON, str, rules=[Pattern(r"^[0-9]{11}$|^[0-9]{12}$")], required= False),
        Param('profile_pic_url', JSON, str, required= False),
        Param('short_desc', JSON, str, required= False),
        Param('long_desc', JSON, str, required= False),
        Param('open_time', JSON, str, rules=[Pattern('^(20)[\d]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$')], required= False),
        Param('close_time', JSON, str, rules=[Pattern('^(20)[\d]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$')], required= False),
        Param('delivery_policy', JSON, str, required= False),
        Param('return_policy', JSON, str, required= False),
        Param('zip_code', JSON, int, required= False),
        Param('address_1', JSON, str, required= False),
        Param('address_2', JSON, str, required= False),
        Param('is_open_weekend', JSON, int, required= False),
        Param('seller_id', JSON, int, required=True)
    )
    def edit_seller(*args):
        connection = None
        change_info = {
            'subcategory_id': args[0],
            'seller_status_id': args[1],
            'seller_name_kr': args[2],
            'seller_name_en': args[3],
            'seller_number': args[4],
            'profile_pic_url': args[5],
            'short_desc': args[6],
            'long_desc': args[7],
            'open_time': args[8],
            'close_time': args[9],
            'delivery_policy': args[10],
            'return_policy': args[11],
            'zip_code': args[12],
            'address_1': args[13],
            'address_2': args[14],
            'is_open_weekend': args[15],
            'seller_id': args[16]
        }
        connection = connect_db()
        user = g.token_info
        if connection:
            account_service = AccountService()
            try:
                change_account = account_service.change_seller_info(change_info, user, connection)
                connection.commit()
                return change_account
            except Exception as e:
                connection.rollback()
                return jsonify({'MESSAGE': f'{e}'}), 400
            finally:
                connection.close()


    @account_app.route('change_seller_status', methods=['PATCH'])
    @login_validator
    @validate_params(
        Param('action_id', JSON, str),
        Param('status_id', JSON, str),
        Param('seller_id', JSON, str)
    )
    def seller_actions(*args):
        connection = None
        status = {
            'action_id': args[0],
            'status_id': args[1],
            'seller_id': args[2]
        }
        user = g.token_info
        connection = connect_db()
        if connection:
            try:
                account_service = AccountService()
                actions = account_service.change_status(status, user, connection)
                connection.commit()
                return jsonify({'status_actions': 'SUCCESS'}), 200
            except Exception as e:
                connection.rollback()
                return jsonify({'MESSAGE': f'{e}'}), 400
            finally:
                connection.close()