### OS ####
import pymysql
### FLASK ###
### USER ###

"""
1. query inputs into cursors will always be called query
2. When inputting data, param is called account_info
3. When using data we already have to filter our data, param is called account_filter
4. function is a verb in present tense
5. A function's output will always be it's past participle
"""



class AccountDao:
    def find_account(self, account_filter, brandiDB):
        with brandiDB.cursor() as cursor:
            query = """
                SELECT
                    id,
                    account_type_id
                FROM
                    accounts
                WHERE
                """
                for keys, values in account_filter.items():
                    if keys == 'email': 
                        query += """
                        email = %(email)s
                        """
                    elif keys == 'id':
                        query += """
                        id = %(id)s

                        """
                    
            cursor.execute(query, account_filter)
            found_account = cursor.fetchone()
            return found_account


    def get_account_password(self, account_filter, brandiDB):
        with brandiDB.cursor() as cursor:
            query = """
                SELECT
                    id,
                    email,
                    password
                FROM
                    accounts
                WHERE
                    id = %(id)s
                """
        cursory.execute(query, account_filter)
        got_account_password = cursor.fetchone
        return got_account_password

    def create_account(self, account_info, brandiDB):
        with brandiDB.cursor() as cursor:
            query = """
                INSERT INTO 
                    accounts(
                    email,
                    password,
                    name,
                    is_active,
                    account_type_id
                    )
                VALUES(
                    %(email)s,
                    %(password)s,
                    %(name)s,
                    1,
                    %(account_type_id)s
                    )
                """
            cursor.execute(query, account_info)
            created_account = cursor.lastrowid
            return created_account

    def update_account_password(self, account_filter, brandiDB)
        with brandiDB.cursor() as cursor:
            query = """
                UPDATE
                    accounts
                SET
                    password = %(password)s
                WHERE
                """
                for keys, values in account_filter.items():
                    if keys == 'email': 
                        query += """
                        email = %(email)s
                        """
                    elif keys == 'id':
                        query += """
                        id = %(id)s
                        """
    def find_seller_