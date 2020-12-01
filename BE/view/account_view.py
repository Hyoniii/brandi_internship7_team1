from flask                   import request, Blueprint,jsonify
from flask.views             import MethodView
from flask_request_validator import (
    GET,
    FORM,
    PATH,
    JSON,
    Param,
    Pattern,
    MinLength,
    MaxLength,
    validate_params
)
from service.account_service import AccountService
from db_connector            import connect_db

"""
WIP 앤드포인트 리스트했어요
"""

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
        Param('name', JSON, str,
            rules=[Pattern(r"^[가-힣]{1,20}$")])
    )
    def sign_up_master(*args):
        connection = None
        account_info = {
            'email': args[0],
            'password': args[1],
            'account_type_id': args[2],
            'name' : args[4]
        }
        
        try:
            connection = connect_db()
            if connection:
                account_service = AccountService()
                signed_up = account_service.signup_account(account_info, connection)
                return signed_up
            else:
                return jsonify({'MESSAGE' : 'NO_DATABASE_CONNECTION'}), 500
        except Exception as e:
            return jsonify({'MESSAGE': f'{e}'}), 500
        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'MESSAGE': f'{e}'}), 500

    @account_app.route('signup/seller', methods=['POST'])
    @validate_params(
        Param('email', JSON, str, rules=[Pattern(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')]),
        Param('password', JSON, str, rules=[MaxLength(80), MinLength(4)]),
        Param('account_type_id', JSON, int),
        Param('account_type_id', JSON, str, rules=[Pattern(r"^[1-2]{1}$")]),
        Param('service_number', JSON, str, rules=[Pattern(r"^\d{3}-\d{3,4}-\d{4}$")]),
        Param('seller_name_kr', JSON, str, rules=[Pattern(r"^[가-힣]{1,20}$")]),
        Param('seller_name_en', JSON, str, rules=[Pattern(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]{1,20}$")]),
        Param('subcategory_id', JSON, str, rules=[Pattern(r"^[1-8]{1}$")])
    )
    def sign_up_seller(*args):
        connection = None
        account_info = {
            'email' : args[0],
            'password' : args[1],
            'account_type_id' : args[2],
            'name' : '미설정'
        }

        seller_info = {
            'account_id' : 1,
            'service_number' : args[4],
            'seller_name_kr' : args[5],
            'seller_name_en' : args[6],
            'subcategory_id' : args[7],
            'seller_status_id' : 1
        }
        
        try:
            connection = connect_db()
            if connection:
                account_service = AccountService()
                seller_signed_up = account_service.signup_seller(seller_info, connection)
                account_signed_up = account_service.signup_account(account_info, connection)
                print(jsonify(account_signed_up))
                connection.commit()
                return jsonify({'seller_id' : seller_signed_up, 'account_id' : account_signed_up}), 200
            else:
                return jsonify({'MESSAGE' : 'NO_DATABASE_CONNECTION'}), 500
        except Exception as e:
            connection.rollback()
            return jsonify({'MESSAGE': f'view{e}'}), 500
        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'MESSAGE': f'view{e}'}), 500

    # @account_app.route('/signin', methods=['POST'])
    # def sign_in():
    #     try:
    #         brandiDB = connect_db()
    #         data = request.json
    #         return brandiDB
    #     except Exception as e:
    #         return jsonify ({'message' : f'{e}'}, 400)

    #     finally:
    #         if brandiDB:
    #             brandiDB.close()

    # @account_app.route('/find', methods=['POST'])
    # def get_user(*args):

    #     db_connection = None

    #     try:
    #         brandiDB = connect_db()
    #         data = request.json

    #         if brandi_DB:
    #             filter_info = {
    #                 'page'            : args[0],
    #                 'limit'           : args[1]
    #             }
    #     except Exception as e:
    #         return jsonify({"message" : f'{e}'}), 400

    #     finally:
    #         if db_connection:
    #             db_connection.close()

    # @account_app.route('/signup', methods=['POST'])
    # def signup():
    #     try:
    #         brandiDB = connect_db()
    #         data = request.json
    #         return brandiDB
    #     except Exception as e:
    #         return jsonify ({'message' : f'{e}'}, 400)

    #     finally:
    #         if brandiDB:
    #             brandiDB.close()

    # @account_app.route('/navbar', methods=['GET'])
    # def NavBar():
    #     try:
    #         brandiDB = connect_db()
    #         data = request.json
    #         return brandiDB ###different navbar items based on user 
    #     except Exception as e:
    #         return jsonify ({'message' : f'{e}'}, 400)

    #     finally:
    #         if brandiDB:
    #             brandiDB.close()

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