### OS ####
### FLASK ###
### USER ###
from config import SECRET_KEY

class AccountService():

    def __init__(self, account_dao, config):
        self.account_dao = account_dao
        self.config      = config

    def signin(self, user_info, ):
        print('2')
    def thou():
        print('a')
        return account_dao.find_user()