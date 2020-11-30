import pymysql
from flask import jsonify,g
from mysql.connector.errors import Error

class ProductDao:

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

                query = '''
                    SELECT 
                        S2.status as seller_status,                        
                        P.created_at as created_at ,
                        I.img_url as image,
                        P.name as product_name,
                        P.code as product_code,
                        P.number as product_number,
                        S3.name as seller_subcategory_name,
                        S.seller_name_kr as seller_name,
                        P.price ,
                        FLOOR(P.price*(100/P.discount_rate)) as discount_price,
                        P.is_selling as is_selling,
                        P.is_visible as is_visible,
                        P.is_discount as is_discount,
                        A.id as account_id           
                    FROM 
                        products as P
                    LEFT JOIN
                        product_images as I
                    ON 
                        P.id = I.product_id
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
                '''
                #seller일 경우 seller의 product만 표출 , validator 완성 후 수정
                if filter_data['account_type_id'] != 1:
                    query += "AND A.id = %(account_id)s"
                # if g.account_info.get('seller_id'):
                #     query += "AND P.seller_id = g.account_info['seller_id']"

                # 등록 기간 시작
                if filter_data.get('started_date', None):
                    query += " AND P.created_at > %(started_date)s"

                # 등록 기간 종료
                if filter_data.get('ended_date', None):
                    query += " AND P.created_at < %(ended_date)s"

                # 셀러명
                if filter_data.get('seller_name', None):
                    query += " AND S.seller_name_kr = %(seller_name)s"

                # 상품명
                if filter_data.get('product_name', None):
                    query += " AND P.name = %(product_name)s"

                # 상품번호
                if filter_data.get('product_number', None):
                    query += " AND P.number = %(product_number)s"

                # 셀러 속성(tuple해서 넘겨야 함)
                if filter_data.get('seller_subcategory_id', None):
                    filter_data['seller_subcategory_id'] = tuple(filter_data['seller_subcategory_id'])
                    query += " AND S.subcategory_id in %(seller_subcategory_id)s"

                # 판매여부
                if filter_data.get('is_selling', None) is not None:
                    query += " AND P.is_selling = %(is_selling)s"

                # 진열여부
                if filter_data.get('is_visible', None) is not None:
                    query += " AND P.is_visible = %(is_visible)s"

                # 할인여부
                if filter_data.get('is_discount', None) is not None:
                    if filter_data['is_discount'] == 1:
                        query += " AND P.is_discount = 1 "
                    elif filter_data['is_discount'] == 0:
                        query += " AND P.is_discount = 0 "

                # 등록순 정렬
                query += " ORDER BY P.created_at DESC"

                cursor.execute(query,filter_data)
                products = cursor.fetchall()

                return products
        # 데이터베이스 error
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
                """

                # master, query string에 담긴 셀러로 탐색
                if filter_data['account_type_id'] == 1:
                    query += "WHERE S.seller_name_kr = %(seller_name)s"

                # seller,디버깅용 하드코딩
                elif filter_data['account_type_id'] == 2:
                    query += "WHERE S.id = %(seller_id)s"

                cursor.execute(query,filter_data)
                filter_categories = cursor.fetchall()

                if filter_categories:
                    # for category in filter_categories:
                    #     main_categories.append(category['name'])
                        return filter_categories
                return jsonify({'message': 'SELLER_CATEGORY_DOES_NOT_EXIST'}), 404
        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def seller_sub_categories(self, main_category_id, connection):
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

                if main_category_id:
                    query += "PC1.id = %(main_category_id)s"

                cursor.execute(query,main_category_id)
                filter_categories = cursor.fetchall()
                print(filter_categories)

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

