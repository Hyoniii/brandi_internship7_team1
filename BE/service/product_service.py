import uuid
import re

from model.product_dao import ProductDao
from flask             import jsonify, g



class ProductService:
    def __init__(self):
        pass

    def get_product_list(self, filter_data, connection):
        product_dao = ProductDao()
        try:
            # 기간 정의
            if filter_data['started_date'] and filter_data['ended_date']:
                if filter_data['ended_date'] < filter_data['started_date']:
                    filter_data['ended_date'] = filter_data['started_date']

            # 두 값이 안들어 왔을 경우 default
            if not filter_data['started_date']:
                filter_data['started_date'] = '2016-05-24'
            if not filter_data['ended_date']:
                filter_data['ended_date'] = '2025-05-24'

            # 기간 데이터 변경
            filter_data['started_date'] += ' 00:00:00'
            filter_data['ended_date'] += ' 23:59:59'

            #limit 범위 설정
            if filter_data['limit'] is None or filter_data['limit'] <= 0:
                filter_data['limit'] = 10

            #page 설정
            if filter_data['page'] is None or filter_data['page'] <= 0:
                filter_data['page'] = 1

            #pagination, offset 생성
            filter_data['offset'] = (filter_data['page'] * filter_data['limit']) - filter_data['limit']

            product_list = product_dao.product_list(filter_data,connection)
            return product_list

        except Exception as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'error': 'DB_CURSOR_ERROR'}), 500


    def product_main_category(self, filter_data, connection):
        """ 상품 1차 카테고리 목록 표출
        seller_categories_type을 기준으로 main 카테고리 보내줌

         Args:
             account_info : 상품 등록시 상품 소유 셀러
             connection   : 데이터베이스 커넥션 객체
        Returns:
            200:셀러에 따른 상품 main 카테고리 목록"""

        product_dao = ProductDao()
        """ 
        g.account_info = {
                        'account_id'      : account_id,
                        'account_type_id' : account['account_type_id'],
                        'seller_id'       : None
                        }
        ------수정 예정------
        # 상품을 등록하는 주체가 마스터이면, query string 에 담긴 셀러 어카운트 넘버로 셀러 선택해서 filter
        if account_type_id == 1:
            #account_id = account_info['account_id']

        # 상품을 등록하는 주체가 셀러이면, 토큰 이용해서 filter
        elif account_type_id == 2:
            # account_id = g.account_info['account_id']
            
        넘겨주는 정보 인자도 바꿔야 함
        """

        # #seller,디버깅용 하드코딩
        # elif filter_data['account_type_id'] == 2:
        #     filter_data['account_id'] = 3
        #     seller_categories = product_dao.seller_main_categories(filter_data, connection)

        # #master, query string에 담긴 셀러로 탐색
        if filter_data.get('seller_name'):
            seller_id                = product_dao.get_seller_id(filter_data,connection)
            filter_data['seller_id'] = seller_id

        main_categories = product_dao.seller_main_categories(filter_data,connection)
        data = {
            'main_categories' : main_categories,
            'seller_id'       : filter_data['seller_id']
        }

        return data

    def product_sub_category(self, filter_data, connection):
        product_dao    = ProductDao()
        sub_categories = product_dao.seller_sub_categories(filter_data, connection)
        return sub_categories

    def get_options(self,connection):
        product_dao = ProductDao()
        colors      = product_dao.get_color_list(connection)
        sizes       = product_dao.get_size_list(connection)
        return {'colors':colors,'sizes':sizes}

    def create_product(self,filter_data,connection):
        product_dao = ProductDao()
        # account_type_id = g.account_info['account_type_id']

        # min,max order 범위 설정
        if filter_data['min_order'] > filter_data['max_order']:
            filter_data['min_order'] = filter_data['max_order']

        # code,number 생성
        filter_data['code'] = uuid.uuid4().hex[:6].upper()
        filter_data['number'] = re.sub("[^0-9]", "", str(uuid.uuid4()) )

        # insert_product
        product_data = product_dao.create_product(filter_data,connection)
        print(product_data)

        # product_log 생성
        product_log = product_dao.create_product_log(product_data,connection)
        print(product_log)




        # 옵션 생성
        product_id  = product_data['product_id']
        options = product_data['option_list']

        [option.insert(0, product_id) or option.append(str(options.index(option) + 1)) for option in options]

        print(options)

        #new_option = product_dao.create_options(options,connection)
        #print(option_count)






        return None










