### OS ####
### FLASK ###
### USER ###
from config import SECRET_KEY

class AccountService():
    def __init__(self, account_dao):
        self.account_dao = account_dao
        print('a')

    def sign_in(self, user_info, brandiDB):
        print('b')
        user = self.user_dao.get_user(user_info, brandiDB)
        if not user:
            return None

        password = self.user_dao.get_user_pw(user, brandiDB)

        if user_info['password'] != int(password):
            return None

        return user