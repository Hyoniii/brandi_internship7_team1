### OS ####
import pymysql
### FLASK ###
### USER ###

"""
1. query inputs into cursors will always be called query
2. When inputting data, param is called _info
3. When using data we already have to filter our data, param is called _filter
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
        cursor.execute(query, account_filter)
        got_account_password = cursor.fetchone
        return got_account_password

    def create_account(self, account_info, brandiDB):
        with brandiDB.cursor() as cursor:
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
            created_account = cursor.lastrowid
            return created_account

    def update_account_info(self, account_filter, brandiDB):

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
                elif keys == 'account_type_id':
                    query += """
                    id = %(id)s
                    """
        cursor.execute(query, account_filter)
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
        cursor.execute(log_query, account_filter)
        updated_account_info_log = cursor.lastrowid
        return updated_account_info_log

    def create_seller(self, seller_info, brandiDB):

        with brandiDB.cursor() as cursor:
            query = """
                INSERT INTO seller(
                    account_id,
                    subcategory_id,
                    seller_status,
                    seller_name_kr,
                    seller_name_en,
                    service_number,
                    profile_pic_url,
                    cover_pic_url,
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
                    )
                VALUES (
                    %(account_id)s,
                    %(subcategory_id)s,
                    %(seller_status)s,
                    %(seller_name_kr)s,
                    %(seller_name_en)s,
                    %(service_number)s,
                    %(profile_pic_url)s,
                    %(cover_pic_url)s,
                    %(short_desc)s,
                    %(long_desc)s,
                    %(open_time)s,
                    %(close_time)s,
                    %(delivery_policy)s,
                    %(return_policy)s,
                    %(zip_code)s,
                    %(address_1)s,
                    %(address_2)s,
                    %(is_open_weekend)s
                )
            """

            cursor.execute(query, seller_info)
            created_seller = cursor.lastrowid

            return created_seller

        with brandiDB.cursor() as cursor:
            query = """
                INSERT INTO seller_logs(
                    account_id,
                    subcategory_id,
                    seller_status,
                    seller_name_kr,
                    seller_name_en,
                    service_number,
                    profile_pic_url,
                    cover_pic_url,
                    short_desc,
                    long_desc,
                    open_time,
                    close_time,
                    delivery_policy,
                    return_policy,
                    zip_code,
                    address_1,
                    address_2,
                    is_open_weekend,
                    editor_id
                    )
                VALUES (
                    %(account_id)s,
                    %(subcategory_id)s,
                    %(seller_status)s,
                    %(seller_name_kr)s,
                    %(seller_name_en)s,
                    %(service_number)s,
                    %(profile_pic_url)s,
                    %(cover_pic_url)s,
                    %(short_desc)s,
                    %(long_desc)s,
                    %(open_time)s,
                    %(close_time)s,
                    %(delivery_policy)s,
                    %(return_policy)s,
                    %(zip_code)s,
                    %(address_1)s,
                    %(address_2)s,
                    %(is_open_weekend)s,
                    %(editor_id)s
                )
                """
            cursor.execute(query, seller_info)
            created_seller_log = cursor.lastrowid

            return created_seller_log


    def update_seller(self, seller_info, brandiDB):

        with brandiDB.cursor() as cursor:
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

        with brandiDB.cursor() as cursor:
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
            cursor.execute(query, account_filter)
            updated_seller_info = cursor.lastrowid
            return updated_seller_info_log


    def find_seller(self, account_filter, brandiDB):

        with brandiDB.cursor() as cursor:
            query = """
                SELECT
                    accounts.id,
                    accounts.account_type_id,
                    accounts.email,
                    sellers.id,
                    sellers.seller_name_kr
                FROM 
                    sellers
                INNER JOIN 
                    accounts
                ON 
                    accounts.id = sellers.account_id
                WHERE
                    id = %(id)s
                """
            cursor.execute(query, account_filter, brandiDB)
            found_seller = cursor.fetchone()
            return found_seller

    
    def list_seller(self, account_filter, brandiDB):

        with brandiDB.cursor() as cursor:
            query = """
                SELECT
                    accounts.id,
                    sellers.id,
                    sellers.subcategory_id,
                    sellers.seller_status_id,
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
                    managers.name AS manager_name,
                    managers.phone_number AS manager_phone_number,
                    managers.email AS manager_email
                FROM 
                    accounts
                LEFT JOIN
                    managers
                ON account.id =







            """