import uuid
import xlsxwriter
import re

from utils             import Product_excel_downloader
from model.product_dao import ProductDao
from config            import S3
from PIL               import Image
from flask             import jsonify, g, send_file


class ProductService:
    def __init__(self):
        pass

    def get_product_list(self, filter_data, connection):
        product_dao = ProductDao()
        try:
            # 상품을 등록하는 주체가 셀러이면, 자기 토큰을 이용해 본인 상품만 표출
            if filter_data['account_type_id'] != 1:
                  filter_data['account_id'] = g.token_info['account_id']

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
            raise e


    def product_main_category(self, filter_data, connection):
        """ 상품 1차 카테고리 목록 표출
        seller_categories_type을 기준으로 main 카테고리 보내줌

         Args:
             account_info : 상품 등록시 상품 소유 셀러
             connection   : 데이터베이스 커넥션 객체
        Returns:
            200:셀러에 따른 상품 main 카테고리 목록"""

        product_dao = ProductDao()

        # seller이면 seller_id 가진다.
        if filter_data['account_type_id'] != 1:
            filter_data['seller_id'] = g.token_info['seller_id']

        # master, query string에 담긴 셀러로 탐색
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

        # min,max order 범위 설정
        if filter_data['min_order']  > filter_data['max_order']:
            filter_data['min_order'] = filter_data['max_order']

        # code,number 생성
        filter_data['code'] = uuid.uuid4().hex[:6].upper()

        # insert_product
        product_data = product_dao.create_product(filter_data,connection)

        # product_log 생성
        product_log = product_dao.create_product_log(product_data,connection)

        # 옵션 생성
        product_id  = product_data['product_id']

        for options in option_list:
            options['product_id'] = product_id
            options['number']     = str(product_id) + str(option_list.index(options)+1)

        create_count = product_dao.create_options(option_list, connection)
        print(create_count)

        return {'create_count' : create_count, 'product_id' : product_id}

    def upload_product_image(self, product_images, product_id, editor_id, connection):
        product_dao = ProductDao()

        #리스트 안에 있는 이미지 딕셔너리 안에 유효 값 추가
        for image in product_images:
            image['product_id'] = product_id
            image['ordering']   = product_images.index(image) + 1
            image['editor_id']  = editor_id
            image['is_deleted'] = 0

        product_dao.create_images(product_images, connection)

        return None

    def product_excel(self, filter_data, connection):
        product_dao = ProductDao()

        try:
            # 기간 정의
            if filter_data['started_date'] and filter_data['ended_date']:
                if filter_data['ended_date']  < filter_data['started_date']:
                    filter_data['ended_date'] = filter_data['started_date']

            # 두 값이 안들어 왔을 경우 default
            if not filter_data['started_date']:
                filter_data['started_date'] = '2016-05-24'
            if not filter_data['ended_date']:
                filter_data['ended_date']   = '2025-05-24'

            # 기간 데이터 변경
            filter_data['started_date'] += ' 00:00:00'
            filter_data['ended_date']   += ' 23:59:59'

            filter_excel_info = product_dao.product_excel_info(filter_data, connection)

            setting_info = Product_excel_downloader.get_product_excel_info(filter_excel_info)

            unique_name = uuid.uuid4().hex[:4].upper()
            file_name   = f'product_list_{unique_name}.xlsx'
            columns     = setting_info['columns']
            excel_info  = setting_info['excel_info']

            workbook    = xlsxwriter.Workbook(file_name)
            worksheet   = workbook.add_worksheet()

            for column in columns:
                worksheet.write(0, columns.index(column), column)

            row = 1
            col = 0

            if g.token_info['account_type_id'] == 1:
                for j in excel_info:
                    worksheet.write(row, col, j.get('created_at'))
                    worksheet.write(row, col + 1, j.get('desc_img_url'))
                    worksheet.write(row, col + 2, j.get('product_name'))
                    worksheet.write(row, col + 3, j.get('product_code'))
                    worksheet.write(row, col + 4, j.get('number'))
                    worksheet.write(row, col + 5, j.get('seller_subcategory_name'))
                    worksheet.write(row, col + 6, j.get('seller_name'))
                    worksheet.write(row, col + 7, j.get('seller_status'))
                    worksheet.write(row, col + 8, j.get('price'))
                    worksheet.write(row, col + 9, j.get('discount_price'))
                    worksheet.write(row, col + 10, j.get('is_selling'))
                    worksheet.write(row, col + 11, j.get('is_visible'))
                    worksheet.write(row, col + 12, j.get('is_discount'))

                    row += 1
            else:
                for j in excel_info:
                    worksheet.write(row, col, j.get('created_at'))
                    worksheet.write(row, col + 1, j.get('desc_img_url'))
                    worksheet.write(row, col + 2, j.get('product_name'))
                    worksheet.write(row, col + 3, j.get('product_code'))
                    worksheet.write(row, col + 4, j.get('number'))
                    worksheet.write(row, col + 5, j.get('price'))
                    worksheet.write(row, col + 6, j.get('discount_price'))
                    worksheet.write(row, col + 7, j.get('is_selling'))
                    worksheet.write(row, col + 8, j.get('is_visible'))
                    worksheet.write(row, col + 9, j.get('is_discount'))

                    row += 1


            workbook.close()

            return send_file(file_name)

        except Exception as e:
            raise e















