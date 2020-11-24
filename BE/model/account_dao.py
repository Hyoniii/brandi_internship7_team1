### OS ####
import pymysql
### FLASK ###
from flask import jsonify
### USER ###

class AccountDao:
    
    def get_user(self, user_info, brandiDB):
        print('a1')
        with brandiDB.cursor() as cursor:
            query = """
                        SELECT
                            id
                        FROM
                            accounts
                        WHERE
                            email = %(email)s
                    """
            cursor.execute(query, user_info)
            user = cursor.fetchone()

            return user

