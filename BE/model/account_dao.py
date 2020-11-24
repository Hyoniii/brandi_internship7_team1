### OS ####
import pymysql
### FLASK ###
### USER ###

class AccountDao:
    def find_user(self, unique_user_info, db_connector):
        with db_connector.cursor() as cursor:
            query = """
                    SELECT
                        id
                        password
                        account_type_id
                    FROM
                        accounts
                    WHERE
                    """
            for key, value in account_filter.items():
                query += """
                    %(key)s = %(value)s
                    """
                    ### I need to append AND to everything after 2
            cursor.execute(account, user_filter)

            account = cursor.fetchall()
            return account

    def create_user(self, account_info, db_connector) :
        with db_connector.cursor() as cursor:
            query = """
                    INSERT INTO accounts (
                                        email,
                                        password,
                                        name,
                                        is_active,
                                        account_type_id
                                ) VALUES(
                                        %(email)s,
                                        %(password)s,
                                        %(name)s,
                                        1,
                                        %(account_type_id)s
                                        )
                    """
            cursor.execute(query, account_info)
            account = cursor.lastrowid
            return account

