### OS ####
### FLASK ###
### USER ###
from config import SECRET_KEY

"""
WIP 앤드포인트 리스트했어요
"""

class AccountService():

    def __init__(self, account_dao, config):
        self.account_dao = account_dao
        self.config      = config

    def signin(self, account_filter, brandiDB):
        """
        1. Open DB
        2. find email or username
        3. get_account
        4. match password(get_account)
        4. return message
        5. close DB 
        """
        ###needs token_validator, get_user, 
    def signup(self, account_info, brandiDB):
        """
        1. Open DB 
        2. create_account
        3. return message
        4. close DB 
        """
        ###needs get_user, create_user
        return account_dao.find_user()
    def change_password(self, user_info, brandiDB):
        """
        1. Open DB
        2. Verify login token
        3. Get account info (verify existence)
        4. Change account info
        5. Return message
        6. Close DB
        """
    def get_account_log(self, user_filter, brandiDB):
        """
        1. Open DB
        2. Check login_token
        3.

        """
        ###needs get_account_log
    def get_seller_log(self, user_filter, brandiDB):
        ###needs get_seller_log
    def get_account_info(self, user_filter, brandiDB):
        ###needs 
    def change_seller_status(self, user_filter, brandiDB):
        ###get_seller_actions, log_info, change_seller_info
    def filter_seller
    def count_seller
    def image_saver
    def count_total_products
    def count_shown_products
    def count_delivered_products
    def products_sold_by_seller
    def revenue_made_by_seller