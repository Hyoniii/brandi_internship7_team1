import pymysql
from flask import jsonify,g
from mysql.connector.errors import Error

class ProductDao:
    def __init__(self):
        pass

    def product_list(self,filter_data,connection):
        """필터링 된 상품 리스트

        Args:
            data       : 필터에 쓰이는 쿼리 정보
            connection : 연결된 데이터베이스 객체

        Return:
            200 : 필터링된 싱품 정보 리스트
            500 : DV_CURSOR_ERROR
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                count_select = """
                SELECT
                    count(P.id) AS count
                """

                list_select = """
                SELECT 
                    P.id as product_id,
                    S2.status as seller_status,                   
                    P.created_at as created_at ,
                    P.name as product_name,
                    P.code as product_code,
                    PO.number as number,
                    I.img_url as Image,
                    S3.name as seller_subcategory_name,
                    S.seller_name_kr as seller_name,
                    P.price ,
                    FLOOR(P.price*(100/P.discount_rate)) as discount_price,
                    P.is_selling as is_selling,
                    P.is_visible as is_visible,
                    P.is_discount as is_discount,
                    A.id as account_id 
                """
                list_from = """
                FROM 
                    products as P 
                LEFT JOIN
                    product_options as PO
                ON
                    PO.product_id = P.id
                LEFT JOIN
                    product_images as I
                ON
                    I.product_id = P.id
                LEFT JOIN
                    sellers as S
                ON 
                    S.id = P.seller_id
                LEFT JOIN
                    seller_statuses as S2
                ON
                    S2.id = S.seller_status_id
                LEFT JOIN
                    seller_subcategories as S3
                ON
                    S3.id = S.subcategory_id
                LEFT JOIN
                    accounts as A
                ON
                    A.id = S.account_id
                WHERE
                    I.ordering = 1
                """
                #seller일 경우 seller의 product만 표출 , validator 완성 후 수정
                if filter_data['account_type_id'] != 1:
                    list_from += """
                    AND A.id = %(account_id)s
                    """
                # if g.account_info.get('seller_id'):
                #     query += "AND P.seller_id = g.account_info['seller_id']"

                # 등록 기간 시작
                if filter_data.get('started_date', None):
                    list_from += """
                     AND P.created_at > %(started_date)s
                     """

                # 등록 기간 종료
                if filter_data.get('ended_date', None):
                    list_from += """
                    AND P.created_at < %(ended_date)s
                    """

                # 셀러명
                if filter_data.get('seller_name', None):
                    list_from += """ 
                    AND S.seller_name_kr = %(seller_name)s
                    """

                # 상품명
                if filter_data.get('product_name', None):
                    list_from += """
                    AND P.name = %(product_name)s
                    """

                # 상품번호
                if filter_data.get('product_number', None):
                    list_from += """
                    AND PO.number = %(product_number)s 
                    """

                # 셀러 속성
                if filter_data.get('seller_subcategory_id', None):
                    list_from += """
                    AND S.subcategory_id in %(seller_subcategory_id)s
                    """

                # 판매여부
                if filter_data.get('is_selling', None) is not None:
                    list_from += """
                    AND P.is_selling = %(is_selling)s
                    """

                # 진열여부
                if filter_data.get('is_visible', None) is not None:
                    list_from += """
                    AND P.is_visible = %(is_visible)s
                    """

                # 할인여부
                if filter_data.get('is_discount', None) is not None:
                    if filter_data['is_discount'] == 1:
                        list_from += """
                        AND P.is_discount = 1
                        """
                    elif filter_data['is_discount'] == 0:
                        list_from += """
                        AND P.is_discount = 0
                        """

                # id 기준으로 중복 값 제외, 등록순 정렬
                list_from += """
                GROUP BY P.id
                ORDER BY P.created_at DESC
                """

                #pagination
                list_from += """
                LIMIT %(limit)s OFFSET %(offset)s
                """

                #상품 리스트
                query = list_select + list_from
                print(query)
                cursor.execute(query,filter_data)
                product_list = cursor.fetchall()
                print(product_list)

                #count
                query = count_select + list_from
                cursor.execute(query, filter_data)
                total_count = cursor.fetchall()
                print(total_count)

                return {'product_list':product_list,'count':total_count}

                #return {'product_list':product_list,'count':total_count}
        # 데이터베이스 error
        except Exception as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e} finally')
            return jsonify({'error': 'DB_CURSOR_ERROR'}), 500

    def get_seller_id(self,filter_data,connection):
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        S.id as seller_id
                    FROM
                        sellers as S
                    WHERE
                        S.seller_name_kr = %(seller_name)s
                """

                cursor.execute(query, filter_data)
                seller_id = cursor.fetchone()
                return seller_id[0]

        except Exception as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e} finally')
            return jsonify({'error': 'DB_CURSOR_ERROR'}), 500

    def seller_main_categories(self,filter_data,connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    SELECT DISTINCT
                        PC1.name as main_category_name,
                        PC1.id as main_category_id
                    FROM
                        seller_product_categories as SPC
                    LEFT JOIN
                        product_categories as PC1
                    ON
                        PC1.id = SPC.product_category_id
                    LEFT JOIN
                        product_sub_categories as PC2
                    ON
                        PC2.category_id = SPC.product_category_id
                    LEFT JOIN
                        seller_categories as SC1
                    ON
                        SC1.id = SPC.seller_category_id
                    LEFT JOIN
                        seller_subcategories as SC2
                    ON
                        SC2.category_id = SC1.id
                    LEFT JOIN
                        sellers as S
                    ON
                        S.subcategory_id = SC2.id
                    WHERE S.id = %(seller_id)s
                """

                # # master, query string에 담긴 셀러로 탐색
                # if filter_data['account_type_id'] == 1:
                #     query += """
                #     WHERE S.seller_name_kr = %(seller_name)s
                #     """
                #
                # # seller,디버깅용 하드코딩
                # elif filter_data['account_type_id'] == 2:
                #     query += """
                #     WHERE S.id = %(seller_id)s
                #     """

                cursor.execute(query,filter_data)
                filter_categories = cursor.fetchall()

                if filter_categories:
                    return filter_categories
                return jsonify({'message': 'SELLER_CATEGORY_DOES_NOT_EXIST'}), 404
        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def seller_sub_categories(self, filter_data, connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    SELECT
                        PC2.name,
                        PC2.id
                    FROM
                        product_sub_categories as PC2
                    LEFT JOIN
                        product_categories as PC1
                    ON
                        PC2.category_id = PC1.id    
                    """

                if filter_data.get('main_category_id',None):
                    query += """
                    WHERE PC1.id = %(main_category_id)s
                    """
                    print(query)
                cursor.execute(query,filter_data)
                filter_categories = cursor.fetchall()

                return filter_categories

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def get_color_list(self,connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT 
                    product_colors.color,
                    product_colors.id
                FROM
                    product_colors
                """
                cursor.execute(query)
                color_list = cursor.fetchall()
                return color_list

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500


    def get_size_list(self,connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT 
                    product_sizes.size,
                    product_sizes.id
                FROM
                    product_sizes
                """
                cursor.execute(query)
                size_list = cursor.fetchall()
                return size_list

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500



    def get_code_info(self,product_subcategory_id,connection):
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT
                    PC2.id as sub_id,
                    PC1.id as main_id
                FROM
                    product_sub_categories as PC2
                    
                LEFT JOIN
                    product_categories as PC1
                ON
                    PC1.id = PC2.category_id
                WHERE
                    PC2.id = %s
                """
                cursor.execute(query,product_subcategory_id)
                code_info = list(cursor.fetchone())
                return code_info


        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def create_product(self,filter_data,connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:

                query = """
                INSERT INTO products(
                    seller_id,
                    sub_category_id,
                    name,
                    code,
                    price,
                    is_selling,
                    is_visible,
                    short_desc,
                    desc_img_url,
                    min_order,
                    max_order """
                if filter_data['is_information_notice'] == 1:
                    query += "," \
                    "manufacturer," \
                    "manufacture_date," \
                    "made_in"
                if filter_data['is_discount_period'] == 1:
                     query += "," \
                    "discount_start_datetime," \
                    "discount_end_datetime"
                query += """
                )
                VALUES(
                    %(seller_id)s,
                    %(sub_category_id)s,
                    %(product_name)s,
                    %(code)s, 
                    %(price)s,
                    %(is_selling)s,
                    %(is_visible)s,
                    %(short_description)s,
                    %(desc_img_url)s,
                    %(min_order)s,
                    %(max_order)s"""
                if filter_data['is_information_notice'] == 1:
                    query += "," \
                    "%(manufacturer)s," \
                    "%(manufacture_date)s," \
                    "%(made_in)s"
                if filter_data['is_discount_period'] == 1:
                    query += "," \
                    "%(discount_start_datetime)s," \
                    "%(discount_end_datetime)s"
                query += """
                )
                """

                cursor.execute(query, filter_data)
                product_id = cursor.lastrowid
                filter_data['product_id'] = product_id

                return filter_data

        except KeyError as e:
            raise e

        except Exception as e:
            raise e

    def create_product_log(self,product_data,connection):
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:

                query = """
                INSERT INTO product_logs(
                    product_id,
                    editor_id,
                    seller_id,
                    sub_category_id,
                    name,
                    code,
                    price,
                    is_selling,
                    is_visible,
                    short_desc,
                    desc_img_url,
                    min_order,
                    max_order """
                if product_data['is_information_notice'] == 1:
                    query += "," \
                    "manufacturer," \
                    "manufacture_date," \
                    "made_in"
                if product_data['is_discount_period'] == 1:
                     query += "," \
                    "discount_start_datetime," \
                    "discount_end_datetime"
                query += """
                )
                VALUES(
                    %(product_id)s,
                    %(editor_id)s,
                    %(seller_id)s,
                    %(sub_category_id)s,
                    %(product_name)s,
                    %(code)s, 
                    %(price)s,
                    %(is_selling)s,
                    %(is_visible)s,
                    %(short_description)s,
                    %(desc_img_url)s,
                    %(min_order)s,
                    %(max_order)s"""
                if product_data['is_information_notice'] == 1:
                    query += "," \
                    "%(manufacturer)s," \
                    "%(manufacture_date)s," \
                    "%(made_in)s"
                if product_data['is_discount_period'] == 1:
                    query += "," \
                    "%(discount_start_datetime)s," \
                    "%(discount_end_datetime)s"
                query += """
                )
                """

                cursor.execute(query, product_data)
                #product_log = cursor.fetchall()
                product_log = cursor.rowcount

                return product_log

        except KeyError as e:
            raise e

        except Exception as e:
            raise e



    def create_options(self, option_list, connection):
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO product_options(
                    product_id,
                    color_id,
                    size_id,
                    inventory,
                    number
                )
                VALUES(
                    %(product_id)s,
                    %(color)s,
                    %(size)s,
                    %(inventory)s,
                    %(number)s
                )
                """

                cursor.executemany(query, option_list)
                options_count = cursor.rowcount

                return options_count

        except KeyError as e:
            raise e

        except Exception as e:
            raise e







