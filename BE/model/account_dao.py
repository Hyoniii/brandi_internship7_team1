### OS ####
import pymysql
from mysql.connector.errors import Error
### FLASK ###
from flask import jsonify
### USER ###

"""
1. query inputs into cursors will always be called query
2. When inputting data, param is called _info
3. When using data we already have to info our data, param is called _info
4. function is a verb in present tense
5. A function's output will always be it's past participle
"""

class AccountDao:
    def find_account(self, account_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT
                    id,
                    account_type_id,
                    email,
                    password,
                    is_active
                FROM
                    accounts
                WHERE
                    email = %(email)s
                """

                cursor.execute(query, account_info)
                found_account = cursor.fetchone()
            return found_account

        except KeyError as e:
            print(f'KEY_ERROR {e}')
            return jsonify({'MESSAGE': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DB_ERROR {e}')
            return jsonify({'MESSAGE': 'DB_CURSOR_ERROR'}), 500


    def get_account_password(self, account_info, connection):
        try:
            with connection.cursor() as cursor:
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

                cursor.execute(query, account_info)
                got_account_password = cursor.fetchone
                return got_account_password

        except KeyError as e:
            print(f'KEY_ERROR {e}')
            return jsonify({'MESSAGE': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DB_ERROR {e}')
            return jsonify({'MESSAGE': 'DB_CURSOR_ERROR'}), 500

    def create_account(self, account_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO accounts(
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
            return cursor.lastrowid

    def create_account_log(self, account_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            log_query = """
                INSERT INTO account_logs(
                    email,
                    account_id,
                    account_type_id,
                    editor_id,
                    password,
                    name,
                    is_active
                    )
                VALUES (
                    %(email)s,
                    %(account_id)s,
                    %(account_type_id)s,
                    %(editor_id)s,
                    %(password)s,
                    %(name)s,
                    %(is_active)s
                    )
            """
            cursor.execute(log_query, account_info)
            created_account_log = cursor.lastrowid
            return created_account_log

    def create_seller(self, account_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            seller_query = """
                INSERT INTO sellers(
                    account_id,
                    subcategory_id,
                    seller_status_id,
                    seller_name_kr,
                    seller_name_en,
                    service_number
                    )
                VALUES (
                    %(account_id)s,
                    %(subcategory_id)s,
                    %(seller_status_id)s,
                    %(seller_name_kr)s,
                    %(seller_name_en)s,
                    %(service_number)s
                )
            """
            cursor.execute(seller_query, account_info)
            created_seller = cursor.lastrowid
            return created_seller

    def update_account_info(self, account_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:

                query = """
                    UPDATE
                        accounts
                    SET
                        password = %(password)s
                    WHERE
                    """
                for keys, values in account_info.items():
                    if keys == 'email':
                        query += """
                        email = %(email)s
                        """
                    elif keys == 'id':
                        query += """
                        id = %(id)s
                        """
                    elif keys == 'account_type_id':
                        query += """
                        id = %(id)s
                        """
                    cursor.execute(query, account_info)
                    updated_account_info = cursor.lastrowid
            return updated_account_info

            log_query = """
                    INSERT INTO account_logs(
                        account_id,
                        account_type_id,
                        editor_id,
                        email,
                        password,
                        name,
                        is_active
                        )
                    VALUES (
                        %(account_id)s,
                        %(account_type_id)s,
                        %(editor_id)s,
                        %(email)s,
                        %(password)s,
                        %(name)s,
                        %(is_active)s
                        )
                    """
            cursor.execute(log_query, account_info)
            updated_account_info_log = cursor.lastrowid
            return updated_account_info_log

        except KeyError as e:
            print(f'KEY_ERROR {e}')
            return jsonify({'MESSAGE': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DB_ERROR {e}')
            return jsonify({'MESSAGE': 'DB_CURSOR_ERROR'}), 500


    def update_seller(self, seller_info, connection):

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    UPDATE
                        seller
                    SET
                        account_id = %(account_id)s,
                        subcategory_id = %(subcategory_id)s,
                        seller_status = %(seller_status)s,
                        seller_name_kr = %(seller_name_kr)s,
                        seller_name_en = %(seller_name_en)s,
                        service_number = %(seller_number)s,
                        profile_pic_url = %(profile_pic)s,
                        cover_pic_url = %(cover_pic_url)s,
                        short_desc = %(short_desc)s,
                        long_desc = %(long_desc)s,
                        open_time = %(open_time)s,
                        close_time = %(close_time)s,
                        delivery_policy = %(delivery_policy)s,
                        return_policy = %(return_policy)s,
                        zip_code = %(zip_code)s,
                        address_1 = %(address_1)s,
                        address_2 = %(address_2)s,
                        is_open_weekend = %(is_open_weekend)s,
                    WHERE
                        id = %(id)s

                        """
                cursor.execute(query, seller_info)
                updated_seller_info = cursor.lastrowid
                return updated_seller_info

            with connection.cursor() as cursor:
                query = """
                    UPDATE
                        seller
                    SET
                        account_id = %(account_id)s,
                        subcategory_id = %(subcategory_id)s,
                        seller_status = %(seller_status)s,
                        seller_name_kr = %(seller_name_kr)s,
                        seller_name_en = %(seller_name_en)s,
                        service_number = %(seller_number)s,
                        profile_pic_url = %(profile_pic)s,
                        cover_pic_url = %(cover_pic_url)s,
                        short_desc = %(short_desc)s,
                        long_desc = %(long_desc)s,
                        open_time = %(open_time)s,
                        close_time = %(close_time)s,
                        delivery_policy = %(delivery_policy)s,
                        return_policy = %(return_policy)s,
                        zip_code = %(zip_code)s,
                        address_1 = %(address_1)s,
                        address_2 = %(address_2)s,
                        is_open_weekend = %(is_open_weekend)s,
                        editor_id = %(editor_id)s
                    WHERE
                        id = %(id)s

                        """
                cursor.execute(query, account_info)
                updated_seller_info = cursor.lastrowid
                return updated_seller_info_log

        except KeyError as e:
            print(f'KEY_ERROR {e}')
            return jsonify({'MESSAGE': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DB_ERROR {e}')
            return jsonify({'MESSAGE': 'DB_CURSOR_ERROR'}), 500


    def find_seller(self, seller_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    accounts.id,
                    accounts.account_type_id,
                    accounts.email,
                    sellers.id,
                    sellers.seller_name_kr,
                    sellers.seller_name_en
                FROM 
                    sellers
                INNER JOIN 
                    accounts
                ON 
                    accounts.id = sellers.account_id
                WHERE
                    sellers.id != NULL 
                """
            for keys, values in seller_info.items():
                    if keys == 'email':
                        query += """
                        AND email = %(accounts.email)s
                        """
                    elif keys == 'id':
                        query += """
                        AND id = %(accounts.id)s
                        """
                    elif keys == 'seller_name_kr':
                        query += """
                        AND seller_name_kr = %(accounts.seller_name_kr)s
                        """
                    elif keys == 'seller_name_en':
                        query += """
                        AND seller_name_en = %(accounts.seller_name_en)s
                        """

            cursor.execute(query, seller_info)
            found_seller = cursor.fetchone()
            return found_seller

    def find_seller_name_kr_exist(self, account_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    sellers.id,
                    sellers.seller_name_kr
                FROM 
                    sellers
                WHERE
                    sellers.seller_name_kr = %(seller_name_kr)s 
                """
            cursor.execute(query, account_info)
            found_seller = cursor.fetchone()
            return found_seller

    def find_seller_name_en_exist(self, account_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    sellers.id,
                    sellers.seller_name_en
                FROM 
                    sellers
                WHERE
                    sellers.seller_name_en = %(seller_name_en)s
                """
            cursor.execute(query, account_info)
            found_seller = cursor.fetchone()
            return found_seller


    
    def list_seller(self, account_info, connection):
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT
                        accounts.id,
                        sellers.id,
                        sellers.account_id,
                        sellers.subcategory_id,
                        subcategories.name
                        sellers.seller_status_id,
                        seller_statuses.status
                        sellers.seller_name_kr,
                        sellers.seller_name_en,
                        sellers.service_number,
                        sellers.open_time,
                        sellers.close_time,
                        sellers.delivery_policy,
                        sellers.return_policy,
                        sellers.zip_code,
                        sellers.address_1,
                        sellers.address_2,
                        sellers.is_open_weekend,
                        sellers.created_at,
                        managers.name,
                        managers.phone_number,
                        managers.email,
                        count(*)
                    FROM 
                        sellers
                    LEFT JOIN
                        accounts
                    ON 
                        sellers.account_id = account.id
                    LEFT JOIN
                        managers
                    ON
                        sellers.manager_id = managers.id WHERE managers.prority = 1
                    LEFT JOIN 
                        subcategories
                    ON
                        sellers.subcategory_id = subcategories.name
                    LEFT JOIN
                        seller_statuses
                    ON
                        sellers.seller_status_id = seller_statuses.status
                    """

                query += """
                    WHERE 
                        account.is_active = 1
                    """

                if account_info['account_id']:
                    query += """
                        AND 
                            sellers.account_id = %(account_is)s
                    """
                if account_info['seller_id']:
                    query += """
                        AND
                            seller.id = %(account_is)s
                    """
                if account_info['subcategory_id']:
                    query += """
                        AND
                            subcategories.name = %(subcategory_name)s
                    """
                if account_info['seller_name_kr']:
                    query += """
                        AND
                            seller.seller_name_kr = %(seller_name_kr)s
                    """
                if account_info['seller_name_en']:
                    query += """
                        AND 
                            seller.seller_name_en = %(seller_name_en)s
                    """
                if account_info['seller_name_en']:
                    query += """
                        AND 
                            seller.seller_name_en = %(seller_name_en)s
                    """
                if account_info['created_lower']:
                    query += """
                        AND
                            sellers.created_at <= %(created_lower)s
                    """
                if account_info['created_upper']:
                    query += """
                        AND
                            sellers.created_at <= %(created_upper)s
                    """
                if account_info['manager_name']:
                    query += """
                        AND
                            manager.name <= %(manager_name)s
                    """
                if account_info['seller_status']:
                    query += """
                        AND
                            seller_statuses.status <= %(seller_status)s
                    """
                if account_info['phone_number']:
                    query += """
                        AND
                            managers.phone_number <= %(phone_number)s
                    """
                if account_info['email']:
                    query += """
                        AND
                            managers.email <= %(email)s
                    """

                cursor.execute(query, account_info, connection)
                listed_seller = cursor.fetchone()
                return listed_seller

        except KeyError as e:
            print(f'KEY_ERROR {e}')
            return jsonify({'MESSAGE': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DB_ERROR {e}')
            return jsonify({'MESSAGE': 'DB_CURSOR_ERROR'}), 500
