import bcrypt
import jwt
from datetime import (datetime, timedelta)
from model.account_dao import AccountDao
from config import (SECRET_KEY, ALGORITHM)
from flask import jsonify


class AccountService:
    def signup_account(self, account_info, connection):
        account_dao = AccountDao()

        is_existing_email = account_dao.find_account(account_info, connection)
        if is_existing_email:
            raise Exception('EXISTING_EMAIL')

        bcrypt_password = bcrypt.hashpw(account_info['password'].encode('utf-8'), bcrypt.gensalt())
        account_info['password'] = bcrypt_password

        signed_up_id = account_dao.create_account(account_info, connection)
        account_info['account_id']= signed_up_id
        account_info['editor_id'] = signed_up_id
        account_info['is_active'] = 1
        print(account_info)
        account_dao.create_account_log(account_info, connection)
        return signed_up_id


    def signup_seller(self, account_info, connection):
        account_dao = AccountDao()

        is_existing_email = account_dao.find_account(account_info, connection)
        if is_existing_email:
            raise Exception('EXISTING_EMAIL')

        is_kr_name_taken = account_dao.find_seller_name_kr_exist(account_info, connection)
        if is_kr_name_taken:
            raise Exception('EXISTING_KR_NAME')

        is_en_name_taken = account_dao.find_seller_name_en_exist(account_info, connection)
        if is_en_name_taken:
            raise Exception('EXISTING_EN_NAME')

        bcrypt_password = bcrypt.hashpw(account_info['password'].encode('utf-8'), bcrypt.gensalt())
        account_info['password'] = bcrypt_password

        signed_up_account = account_dao.create_account(account_info, connection)
        account_info['account_id'] = signed_up_account
        signed_up_seller = account_dao.create_seller(account_info, connection)
        return signed_up_seller

    def create_account_log(self, account_info, signed_up_id, connection,*args):
        account_dao = AccountDao()
        signupaccount = signup_account()
        signupseller = signup_seller()

        if signed_up_id:
            account_info['account_id'] = signed_up_id
            account_info['editor_id'] = signed_up_id
            account_info['is_active'] = 1
            print(account_info)

            account_log_id = account_dao.create_account_log(account_info, connection)
            if not signed_up_id:
                raise Exception('LOG_NOT_CREATED')
        return account_log_id

        #
        #     account_logged = account_dao.create_account_log(account_info, connection)
        # except Exception as e:
        #     return jsonify({'MESSAGE' : 'ACCOUNT_NOT_CREATED'}), 400


    def signin(self, login_info, connection):
        account_dao = AccountDao()
        account = account_dao.find_account(login_info, connection)

        if account:
            if account['is_active'] == 1:
                if bcrypt.checkpw(login_info['password'].encode('utf-8'), account['password'].encode('utf-8')):
                    token = jwt.encode({'account_id': account['id'], 'expiration': str(datetime.utcnow() + timedelta(hours=1))}, SECRET_KEY, algorithm=ALGORITHM)
                    print(token)
                    return jsonify({'AUTHORIZATION' : token})
                else:
                    raise Exception('PASSWORD_INCORRECT')
            else:
                raise Exception('ACCOUNT_NOT_ACTIVE')
        else:
            raise Exception('ACCOUNT_DOES_NOT_EXIST')

    def filter_seller(self, filter_info, user, connection):
        account_dao = AccountDao()
        account_type_id = user.get('account_type_id')
        if account_type_id == 1:
            seller_list = account_dao.list_seller(filter_info, connection)
            return seller_list
        else:
            raise Exception('NO_MASTER_AUTH')



    #     """
    #     1. Open DB 
    #     2. create_account
    #     3. return message
    #     4. close DB 
    #     """
    #     ###needs get_user, create_user
    #     return account_dao.find_user()
    # def change_password(self, user_info, connection):
    #     """
    #     1. Open DB
    #     2. Verify login token
    #     3. Get account info (verify existence)
    #     4. Change account info
    #     5. Return message
    #     6. Close DB
    #     """
    # def get_account_log(self, user_filter, connection):
    #     """
    #     1. Open DB
    #     2. Check login_token
    #     3.

    #     """
    #     ###needs get_account_log
    # def get_seller_log(self, user_filter, connection):
    #     ###needs get_seller_log
    # def get_account_info(self, user_filter, connection):
    #     ###needs 
    # def change_seller_status(self, user_filter, connection):
    #     ###get_seller_actions, log_info, change_seller_info
    # def filter_seller
    # def count_seller
    # def image_saver
    # def count_total_products
    # def count_shown_products
    # def count_delivered_products
    # def products_sold_by_seller
    # def revenue_made_by_seller
