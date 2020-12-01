<<<<<<< HEAD
import bcrypt

from model.account_dao import AccountDao
from flask             import jsonify

class AccountService:
    # def get_first_categories(self,account_info,db_connection):
    #     """  상품 1차 카테고리 목록 표출
    #
    #     seller 마다 다른
    #     """

    def signup_account(self, account_info, connection):
        account_dao = AccountDao()

        try:
            is_existing_account = account_dao.find_account(account_info, connection)
            if is_existing_account:
                return jsonify({'MESSAGE': 'EXISTING_ID'}), 400

            bcrypted_password = bcrypt.hashpw(account_info['password'].encode('utf-8'), bcrypt.gensalt())
            account_info['password'] = bcrypted_password

            signed_up = account_dao.create_account(account_info, connection)
            print(type(signed_up))
            print(signed_up['ID']['account'])

            return jsonify({'MESSAGE' : 'master_account_created', 'ID' : signed_up}), 200

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def signup_seller(self, seller_info, connection):
        account_dao = AccountDao()

        try:

            is_kr_name_taken = account_dao.find_seller(seller_info, connection)
            if is_kr_name_taken:
                return jsonify({'MESSAGE': 'EXISTING_NAME'}), 400

            is_en_name_taken = account_dao.find_seller(seller_info, connection)
            if is_en_name_taken:
                return jsonify({'MESSAGE' : 'EXISTING_NAME'}), 400

            bcrypted_password = bcrypt.hashpw(account_info['password'].encode('utf-8'), bcrypt.gensalt())
            account_info['password'] = bcrypted_password

            signed_up_account = account_dao.create_account(account_info, connection)
            print(sign_up_account['ID']['account'])
            signed_up_seller = account_dao.create_seller(seller_info, connection)
            return jsonify({'MESSAGE' : 'seller_and_account_created' , 'account_ids' : signed_up}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': f'dao{e}'}), 500




    # def signin(self, account_info, connection):

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