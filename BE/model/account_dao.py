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
                        service_number,
                        profile_pic_url,
                        short_desc,
                        long_desc,
                        close_time,
                        open_time,
                        delivery_policy,
                        return_policy,
                        zip_code,
                        address_1,
                        address_2,
                        is_open_weekend
                        )
                    VALUES (
                        %(seller_id)s,
                        %(subcategory_id)s, 
                        %(seller_status_id)s, 
                        %(editor_id)s, 
                        %(seller_name_kr)s, 
                        %(seller_name_en)s,
                        %(service_number)s,
                        %(profile_pic_url)s,
                        %(short_desc)s,
                        %(long_desc)s,
                        %(close_time)s,
                        %(open_time)s,
                        %(delivery_policy)s,
                        %(return_policy)s,
                        %(zip_code)s,
                        %(address_1)s,
                        %(address_2)s,
                        %(is_open_weekend)s
                    )
                """
                cursor.execute(query, account_info)
                created_seller_log = cursor.fetchone()
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
                query += """
                    WHERE
                        id = %(id)s
                    """
                update_account_info_check = cursor.execute(query, change_info)
                if not update_account_info_check:
                    raise Exception("update fail")

                return cursor.rowcount

        except KeyError as e:
            return jsonify({'MESSAGE': f'DAO_update_account_info{e}'}), 500

        except Error as e:
            return jsonify({'MESSAGE': f'DAO_update_account_info{e}'}), 500

    def update_seller(self, change_info, connection):

        # try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    sellers
                SET
            """
            if change_info['subcategory_id']:
                query += 'subcategory_id = %(subcategory_id)s,'
            if change_info['seller_status_id']:
                query += 'seller_status_id = %(seller_status)s,'
            if change_info['seller_name_kr']:
                query += 'seller_name_kr = %(seller_name_kr)s,'
            if change_info['seller_name_en']:
                query += 'seller_name_en = %(seller_name_en)s,'
            if change_info['seller_number']:
                query += 'service_number = %(seller_number)s,'
            if change_info['profile_pic_url']:
                query += 'profile_pic_url = %(profile_pic_url)s,'
            if change_info['short_desc']:
                query += 'short_desc = %(short_desc)s,'
            if change_info['long_desc']:
                query += 'long_desc = %(email)s,'
            if change_info['open_time']:
                query += 'open_time = %(open_time)s,'
            if change_info['close_time']:
                query += 'close_time = %(close_time)s,'
            if change_info['delivery_policy']:
                query += 'delivery_policy = %(delivery_policy)s,'
            if change_info['return_policy']:
                query += 'return_policy= %(return_policy)s,'
            if change_info['zip_code']:
                query += 'zip_code = %(zip_code)s,'
            if change_info['address_1']:
                query += 'address_1 = %(address_1)s,'
            if change_info['address_2']:
                query += 'address_2 = %(address_2)s,'
            if change_info['is_open_weekend']:
                query += 'is_open_weekend = %(is_open_weekend)s,'
            query = query[:-1]
            query += """
                WHERE
                    id = %(id)s
                """
            cursor.execute(query, change_info)
            updated_seller_info = cursor.lastrowid
            return updated_seller_info
        #
        # except KeyError as e:
        #     return jsonify({'MESSAGE': f'DAO_update_seller{e}'}), 500
        #
        # except Error as e:
        #     return jsonify({'MESSAGE': f'DAO_update_seller{e}'}), 500

    def get_seller_info(self, seller_info, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT
                    id,
                    subcategory_id,
                    seller_status_id,
                    seller_name_kr,
                    seller_name_en,
                    service_number,
                    profile_pic_url,
                    short_desc,
                    long_desc,
                    open_time,
                    close_time,
                    delivery_policy,
                    return_policy,
                    zip_code,
                    address_1,
                    address_2,
                    is_open_weekend
                FROM
                    sellers
                WHERE
                    id = %(id)s     
                """
                cursor.execute(query, seller_info)
                got_account_info = cursor.fetchone()
                return got_account_info
        except KeyError as e:
            raise Exception(f'DAO_get_seller_info_keyerror{e}')
        except Error as e:
            raise Exception(f'DAO_get_seller_info_error{e}')

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
                    accounts.id AS account_id,
                    accounts.email AS account_email,
                    accounts.is_active AS is_active,
                    sellers.id AS seller_id,
                    sellers.subcategory_id AS subcategory_id,
                    seller_subcategories.name AS subcategory_name,
                    seller_statuses.status AS seller_status,
                    seller_statuses.id AS seller_status_id,
                    sellers.seller_name_kr AS korean_label,
                    sellers.seller_name_en AS english_label,
                    sellers.service_number AS seller_number,
                    sellers.created_at AS join_date,
                    managers.name AS manager_name,
                    managers.phone_number AS manager_phone,
                    managers.email AS manager_email
                FROM 
                    sellers
                LEFT JOIN
                    accounts
                ON 
                    sellers.account_id = accounts.id
                LEFT JOIN
                    managers
                ON
                    accounts.id = managers.seller_id
                LEFT JOIN 
                    seller_subcategories
                ON
                    sellers.subcategory_id = seller_subcategories.id
                LEFT JOIN
                    seller_statuses
                ON
                    sellers.seller_status_id = seller_statuses.id
                WHERE 
                    accounts.is_active = 1
            """
            if filter_info['account_id']:
                query += """
                AND
                    accounts.id = %(account_id)s
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
                    manager.name = %(manager_name)s
                """
            if filter_info['seller_status']:
                query += """
                AND
                    seller_statuses.status = %(seller_status)s
                """
            if filter_info['manager_phone']:
                query += """
                AND
                    managers.phone_number = %(manager_phone)s
                """
            if filter_info['email']:
                query += """
                AND
                    managers.email = %(email)s
                """
            if filter_info['order_by']:
                query += """
                ORDER BY sellers.created_at %(order_by)s
                """
            elif not filter_info['order_by']:
                query += """
                ORDER BY sellers.created_at DESC
                """
            query += """
                LIMIT %(limit)s OFFSET %(offset)s
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

    def get_seller_actions(self, status, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                seller_statuses.id AS status_id,
                seller_statuses.status AS status_name,
                status_actions.action_id AS action_id,
                actions.name AS action_name,
                status_actions.status_after_action_id AS new_status_id
                
            FROM
                status_actions
            LEFT JOIN
                actions
            ON
                status_actions.action_id = actions.id
            LEFT JOIN
                seller_statuses
            ON
                status_actions.status_id = seller_statuses.id
            WHERE
                status_id = %(status_id)s
            """
            cursor.execute(query, status)
            return cursor.fetchall()

    def get_seller_actions_two(self, status, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                seller_statuses.id AS status_id,
                seller_statuses.status AS status_name,
                status_actions.action_id AS action_id,
                actions.name AS action_name,
                status_actions.status_after_action_id AS new_status_id

            FROM
                status_actions
            LEFT JOIN
                actions
            ON
                status_actions.action_id = actions.id
            LEFT JOIN
                seller_statuses
            ON
                status_actions.status_id = seller_statuses.id
            WHERE
                status_id = %(status_id)s
            AND
                action_id = %(action_id)s
            """
            cursor.execute(query, status)
            return cursor.fetchall()

    def update_seller_status(self, change_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                UPDATE
                    sellers
                SET
                    seller_status_id = %(seller_status)s
                WHERE
                    id = %(id)s
                """
            cursor.execute(query, change_info)
            updated_seller_info = cursor.lastrowid
            return updated_seller_info