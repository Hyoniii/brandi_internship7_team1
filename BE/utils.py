import os, io, jwt, uuid

from flask        import request, jsonify, g 
from db_connector import connection
from PIL          import image 
from config       import SECRET_KEY, ALGORITHM


def login_validator:
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('AUTHORIZATION', None)

        if access_token:
            try:
                data = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                account_id = data['account_id']
                connection = connect_db()

                if connection:
                    try:
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            query = """
                                SELECT
                                    accounts.account_type_id,
                                    accounts.is_active,
                                    accounts.id,
                                    sellers.account_id
                                    sellers.id as seller_id
                                FROM
                                    accounts
                                INNER JOIN
                                    sellers ON sellers.account_id = account.id
                                WHERE
                                    accounts.id = %(account_id)s
                            """
                        cursor.execute(query, {'account_id': account_id})
                        account = connection.fetchone()
                        if account:
                            if account['is_active'] == 1 and account['account_type_id'] == 1:
                                g.toke_info = {
                                    'account_id': account_id,
                                    'account_type_id' : account['account_type_id'],
                                    'seller_id' : None}
                            if account['is_active'] == 1 and account['account_type_id'] == 2:
                                g.token_info = {
                                    'account_id': account_id,
                                    'account_type_id' : account['account_type_id'],
                                    'seller_id' : account['seller_id']
                                    }
                                return func(*args, **kwargs)
                            return jsonify({'MESSAGE' : 'account_not_active'}), 400
                        return jsonify({'MESSAGE' : 'account_nonexistant'}), 404
                except Error as e:
                    print (f'DATABASE_CURSOR_ERROR {e}')
                    return Jsonify({'MESSAGE' : 'DB_error'}), 400
            except jwt.InvalidTokenError:
                return jsonify({'MESSAGE' : 'invalid_token'}), 401

            return jsonify({'MESSAGE' : 'no_db_connection'}), 400
        return jsonify({'MESSAGE' : 'invalid_token'}), 401
    return wrapper
