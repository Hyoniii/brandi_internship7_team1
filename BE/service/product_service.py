from model.product_dao import ProductDao
from flask             import jsonify, g

class ProductService:

    def get_product_list(self, filter_data, connection):
        product_dao = ProductDao()
        try:
            product_list = product_dao.product_list(filter_data,connection)

            #pagination
            page_size = filter_data['limit']
            limit = filter_data['page'] * page_size
            offset = limit - page_size
            page_list = product_list[offset:limit]

            return page_list

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
                        'account_id': account_id,
                        'account_type_id' : account['account_type_id'],
                        'seller_id' : None
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

        # #master, query string에 담긴 셀러로 탐색
        # if filter_data['account_type_id'] == 1:
        #     seller_categories = product_dao.seller_main_categories(filter_data,connection)
        #
        # #seller,디버깅용 하드코딩
        # elif filter_data['account_type_id'] == 2:
        #     filter_data['account_id'] = 3
        #     seller_categories = product_dao.seller_main_categories(filter_data, connection)

        main_categories = product_dao.seller_main_categories(filter_data,connection)
        return main_categories

    def product_sub_category(self, main_category_id, connection):
        product_dao = ProductDao()
        sub_categories = product_dao.seller_sub_categories(main_category_id, connection)
        print(main_category_id)


