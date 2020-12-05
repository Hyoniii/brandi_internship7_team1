import uuid
import re

from model.product_dao import ProductDao
from config            import S3
from PIL               import Image
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

            products = product_list['product_list']
            counts   = product_list['count']
            #Group by로 grouping 해서 중복 값 제거함
            count    = len(counts)


            return {'product_list' : products, 'count' : count}

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

    def create_product(self, filter_data, option_list, connection):
        product_dao = ProductDao()
        # account_type_id = g.account_info['account_type_id']

        # min,max order 범위 설정
        if filter_data['min_order'] > filter_data['max_order']:
            filter_data['min_order'] = filter_data['max_order']

        # code,number 생성
        filter_data['code'] = uuid.uuid4().hex[:6].upper()
        #filter_data['number'] = re.sub("[^0-9]", "", str(uuid.uuid4()) )


        # insert_product
        product_data = product_dao.create_product(filter_data,connection)
        print("product_create",product_data)


        # product_log 생성
        product_log = product_dao.create_product_log(product_data,connection)
        print("product_log", product_log)

        # 옵션 생성
        product_id  = product_data['product_id']

        for options in option_list:
            options['product_id'] = product_id
            options['number'] = str(product_id) + str(option_list.index(options))

        # [option.insert(0, product_id) for option in options]
        #
        # for i in range(len(options)):
        #     options[i].append(str(options[i][0])+str(i))

        create_count = product_dao.create_options(option_list, connection)
        print("yeeeeeeeeeeeeee",create_count)
        return create_count

    def upload_product_image(self, images, product_id, s3_connection, connection):
        product_images = {}

        try:
            for num in range(1,6):

                #대표사진 미등록 예외처리
                if 'product_image_1' not in images:
                    raise Exception('THUMBNAIL_IMAGE_IS_REQUIRED')

                #상품사진 미정렬 예외처리
                if num > 2:
                    if(f'product_image_{num}' in images) and (f'product_image_{num-1}' not in images):
                        raise Exception('IMAGE_CAN_ONLY_REGISTER_IN_ORDER')

                # 상품사진 있는 경우 product_images Dictionary에 저장
                if f'product_image_{num}' in images:
                    product_images[images[f'product_image_{num}'].name] = images.get(f'product_image_{num}',
                                                                                     None)

                    # 파일이 Image가 아닌 경우 Exception 발생
                    image = Image.open(product_images[f'product_image_{num}'])
                    width, height = image.size

                    # 사이즈가 너무 작은 경우 예외처리
                    if width < 640 or height < 720:
                        raise Exception('IMAGE_SIZE_IS_TOO_SMALL')

            # image file name에 등록되는 product_code 조회
            product_code = self.product_dao.select_product_code(product_id, db_connection)

            # 상품 이미지 받아오기 및 유효성 검사 이후 S3 upload
            resizing = ResizeImage(product_code['product_code'], product_images, s3_connection)
            resized_image = resizing()

            # 사진크기 별 product_image(최대 5개)에 대해 image URL insert & product_images(매핑테이블) insert
            for product_image_no, image_url in resized_image.items():
                image_no = self.product_dao.insert_image(image_url, db_connection)
                self.product_dao.insert_product_image(product_id, image_no, product_image_no, db_connection)

            return None




        except Exception as e:
            raise e
















