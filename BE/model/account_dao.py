import pymysql
from mysql.connector.errors import Error
from flask import jsonify


class AccountDao:
    def __init__(self):
        pass

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
            raise Exception(f'DAO_find_account_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_find_account_error{e}')

    def get_account_info(self, account_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT
                    id,
                    email,
                    account_type_id,
                    password,
                    name,
                    is_active
                FROM
                    accounts
                WHERE
                    id = %(id)s     
                """
                cursor.execute(query, account_info)
                got_account_info = cursor.fetchone()
                return got_account_info
        except KeyError as e:
            raise Exception(f'DAO_get_account_info_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_get_account_info_error{e}')

    def get_account_password(self, account_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
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
            raise Exception(f'DAO_get_account_password_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_get_account_password_error{e}')

    def create_account(self, account_info, connection):
        try:
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
        except KeyError as e:
            raise Exception(f'DAO_create_account_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_create_account_password_error{e}')

    def create_account_log(self, account_info, connection):
        try:
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

        except KeyError as e:
            raise Exception(f'DAO_create_account_log_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_create_account_log_error{e}')

    def create_seller(self, account_info, connection):
        try:
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

        except KeyError as e:
            raise Exception(f'DAO_create_seller_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_create_seller_error{e}')

    def create_seller_log(self, account_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    INSERT INTO seller_logs(
                        seller_id,
                        subcategory_id,
                        seller_status_id,
                        editor_id,
                        seller_name_kr,
                        seller_name_en,
                        service_number
                        )
                    VALUES (
                        %(seller_id)s,
                        %(subcategory_id)s, 
                        %(seller_status_id)s, 
                        %(editor_id)s, 
                        %(seller_name_kr)s, 
                        %(seller_name_en)s,
                        %(service_number)s
                    )
                    
                """
                cursor.execute(query, account_info)
                created_seller_log = cursor.lastrowid
                return created_seller_log
        except KeyError as e:
            raise Exception(f'DAO_create_seller_log_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_create_seller_log_error{e}')

    def update_account_info(self, change_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    UPDATE
                        accounts
                    SET
                """
                if change_info['email']:
                    query += 'email = %(email)s,'
                if change_info['password']:
                    query += "password = %(password)s,"
                if change_info['name']:
                    query += "name = %(name)s,"
                if change_info['is_active']:
                    query += "is_active = %(is_active)s,"
                if change_info['account_type_id']:
                    query += "account_type_id = %(account_type_id)s,"
                query = query[:-1]
                print(query)
                query += """
                    WHERE
                        id = %(id)s
                    """
                print(1)
                print(query)
                update_account_info_check = cursor.execute(query, change_info)
                if not update_account_info_check:
                    raise Exception("update fail")

                return cursor.rowcount

        except KeyError as e:
            return jsonify({'MESSAGE': f'DAO_update_account_info{e}'}), 500

        except Error as e:
            return jsonify({'MESSAGE': f'DAO_update_account_info{e}'}), 500

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

        except KeyError as e:
            print(f'KEY_ERROR {e}')
            return jsonify({'MESSAGE': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DB_ERROR {e}')
            return jsonify({'MESSAGE': 'DB_CURSOR_ERROR'}), 500

    def find_seller(self, seller_info, connection):
        try:
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

        except KeyError as e:
            raise Exception(f'DAO_create_find_seller_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_create_find_seller_error{e}')

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

    def list_seller(self, filter_info, connection):

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    accounts.id,
                    accounts.email,
                    accounts.is_active,
                    sellers.id,
                    sellers.account_id,
                    sellers.subcategory_id,
                    seller_subcategories.name,
                    sellers.seller_status_id,
                    seller_statuses.status,
                    sellers.seller_name_kr,
                    sellers.seller_name_en,
                    sellers.service_number,
                    sellers.created_at,
                    managers.name,
                    managers.phone_number,
                    managers.email,
                    COUNT(*) as filtered_items_count
                FROM 
                    sellers
                LEFT JOIN
                    accounts
                ON 
                    sellers.account_id = accounts.id
                RIGHT JOIN
                    managers
                ON
                    accounts.id = managers.seller_id
                LEFT JOIN 
                    seller_subcategories
                ON
                    sellers.subcategory_id = seller_subcategories.name
                LEFT JOIN
                    seller_statuses
                ON
                    sellers.seller_status_id = seller_statuses.status
                WHERE 
                    accounts.is_active = 1
                AND
                    managers.priority = 1
            """

            if filter_info['account_id']:
                query += """
                AND 
                    sellers.account_id = %(account_id)s
                """
            if filter_info['email']:
                query += """
                AND
                    accounts.email = %(email)s
                """
            if filter_info['seller_id']:
                query += """
                AND
                    sellers.id = %(seller_id)s
                """
            if filter_info['seller_category']:
                query += """
                AND
                    subcategories.name = %(seller_category)s
                """
            if filter_info['seller_kr']:
                query += """
                AND
                    seller.seller_name_kr = %(seller_kr)s
                """
            if filter_info['seller_en']:
                query += """
                AND 
                    seller.seller_name_en = %(seller_en)s
                """
            if filter_info['created_lower']:
                query += """
                AND
                    sellers.created_at <= %(created_lower)s
                """
            if filter_info['created_upper']:
                query += """
                AND
                    sellers.created_at <= %(created_upper)s
                """
            if filter_info['manager_name']:
                query += """
                AND
                    manager.name <= %(manager_name)s
                """
            if filter_info['seller_status']:
                query += """
                AND
                    seller_statuses.status <= %(seller_status)s
                """
            if filter_info['manager_phone']:
                query += """
                AND
                    managers.phone_number <= %(manager_phone)s
                """
            if filter_info['email']:
                query += """
                AND
                    managers.email <= %(email)s
                """
            if filter_info['order_by']:
                if filter_info['order_by'] == 'desc':
                    query += """
                ORDER BY sellers.created_at DESC
                """
                else:
                    query += """
                ORDER BY sellers.created_at ASC
                """
            elif not filter_info['order_by']:
                query += """
                ORDER BY sellers.created_at DESC LIMIT %(limit)s OFFSET %(offset)s
                    """

            cursor.execute(query, filter_info)
            listed_seller = cursor.fetchall()
            return listed_seller

    def get_seller_types(self, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                id,
                name
            FROM seller_subcategories
            """
            cursor.execute(query)
            return cursor.fetchall()
