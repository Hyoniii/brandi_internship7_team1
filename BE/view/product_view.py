import json, io
import datetime

from flask                   import request, Blueprint, jsonify, g

from service.product_service import ProductService
from utils                   import login_validator, Image_uploader, Product_excel_downloader
from db_connector            import connect_db, get_s3_connection
from flask_request_validator import (
    GET,
    FORM,
    JSON,
    PATH,
    Param,
    Pattern,
    Enum,
    validate_params
)

class ProductView:
    product_app = Blueprint('product_app', __name__, url_prefix='/products')

    @product_app.route('', methods=['GET'])
    @login_validator
    @validate_params(
        Param('started_date', GET, str, required=False,
              rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('ended_date', GET, str, required=False,
              rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('product_number', GET, str, required=False),
        Param('product_code', GET, str, required=False),
        Param('seller_subcategory_id', GET, list, required=False),
        Param('is_selling', GET, bool, rules=[Enum(0, 1)], required=False),
        Param('is_visible', GET, bool, rules=[Enum(0, 1)], required=False),
        Param('is_discount', GET, bool, rules=[Enum(0, 1)], required=False),
        Param('limit', GET, int, rules=[Enum(10, 20, 50)], required=False),
        Param('page', GET, int, required=False),
        )
    def get_product_list(*args):
        connection = None

        """상품 리스트 엔드포인트
        상품 관리 페이지에서 필터링된 상품 리스트를 표출
        쿼리 파라미터로 필터링에 사용할 파라미터 값을 받음     
        
        Return:
            200: 상품 리스트
            403: NO_AUTHORIZATION
            500: NO_DATABASE_CONNECTION, DB_CURSOR_ERROR
                 NO_DATABASE_CONNECTION
        History:
            2020-11-28 : 초기 생성
            2020-11-19 : pagination 수정
                 
        수정할 사항
        @login_validator로 g.account_info 받을 예정
            g.account_info ={
                'account_id' :  ,
                'account_type_id' :  ,
                'seller_id' : id or None
            }
        """

        #유효성 검사 완료한 쿼리 값 저장
        filter_data = {
            'started_date'          : args[0],
            'ended_date'            : args[1],
            'seller_name'           : args[2],
            'product_name'          : args[3],
            'product_number'        : args[4],
            'product_code'          : args[5],
            'seller_subcategory_id' : args[6],
            'is_selling'            : args[7],
            'is_visible'            : args[8],
            'is_discount'           : args[9],
            'limit'                 : args[10],
            'page'                  : args[11],
            'account_type_id'       : g.token_info['account_type_id']
        }

        try:
            connection = connect_db()

            if connection:
                product_service = ProductService()
                products        = product_service.get_product_list( filter_data, connection )
                return jsonify(products),200
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 400

        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/category', methods=['GET'])
    @login_validator
    @validate_params(
        Param('seller_name', GET, str, required=False))
    def get_main_category(*args):

        """ 상품 분류별 main 카테고리 표출 엔드포인트
        - master이면 seller검색
        - seller이면 validator 본인 id

        Return:
            200: 셀러가 속한 상품 분류에 따른 1차 카테고리 이름과 id
                 {  "main_category_id": 8,
                    "main_category_name": "주얼리"}
            400: 데이터베이스 연결 에러
            500: server error"""
        connection = None
        # 마스터인데 셀러이름 검색 안한 경우(커넥션 열기전에 처리해줌)
        if g.token_info['account_type_id'] == 1 and args[0] is None:
            return jsonify({'message': 'SELLER_CATEGORY_SEARCHING_ERROR'}), 400

        try:
            connection = connect_db()
            if connection:

                filter_data = {
                    'account_type_id': g.token_info['account_type_id'],
                    'seller_name'    : args[0]
                }

                product_service = ProductService()
                main_categories_data = product_service.product_main_category(filter_data, connection)
        except Exception as e:
            return jsonify({'message' : f'{e}'}), 400
        else:
            return jsonify(main_categories_data), 200
        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/category/<int:main_category_id>', methods=['GET'])
    @login_validator
    @validate_params(
        Param('main_category_id', PATH, int),
        #유효한 카테고리 범위 벗어날 시 에러 반환
        Param('main_category_id', PATH, str, rules=[Pattern(r'^([0-9]|[0-3][0-9])$')]),
    )
    def get_sub_category(*args):
        """ 상품 분류별 sub 카테고리 목록 표출 엔드포인트
        Args:
            *args:
                main_category_id(int): 1차 카테고리 인덱스 번호
        """
        connection = None

        #쿼리 스트링에 값이 없으면 에러 반환
        if args[0] is None:
            return jsonify({'message': 'MAIN_CATEGORY_ID_ERROR'}), 400

        try:
            connection = connect_db()

            if connection:
                filter_data = {
                    'main_category_id' : args[0]
                }
                product_service = ProductService()
                sub_categories  = product_service.product_sub_category(filter_data, connection)

                return jsonify({'data':sub_categories}), 200
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 400

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/register', methods=['GET'])
    def get_option_list(*args):
        connection = None
        try:
            connection = connect_db()
            if connection:
                product_service = ProductService()
                options         = product_service.get_options(connection)
                return options
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500
        finally:
            try:
                connection.close()

            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/register', methods=['POST'])
    @login_validator
    @validate_params(
        Param('is_selling', FORM, int, rules=[Enum(0, 1)]),
        Param('is_visible', FORM, int, rules=[Enum(0, 1)]),
        Param('sub_category_id', FORM, int, required=False),
        Param('product_name', FORM, str,
              rules=[Pattern(r"[^\"\']")]),
        Param('is_information_notice', FORM, int, rules=[Enum(0, 1)]),
        Param('manufacturer', FORM, str, required=False),
        Param('manufacture_date', FORM, str, required=False, rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('made_in', FORM, str, required=False),
        Param('short_description', FORM, str, required=False),
        Param('is_inventory_management', FORM, int, rules=[Enum(0, 1)]),
        Param('inventory', FORM, int, required=False),
        Param('price', FORM, int),
        Param('discount_rate', FORM, float, required=False),
        Param('is_discount_period', FORM, int, rules=[Enum(0, 1)]),
        Param('discount_start_time', FORM, str, required=False),
        Param('discount_end_time', FORM, str, required=False),
        Param('min_order', FORM, int),
        Param('max_order', FORM, int),
        Param('seller_id', FORM, int, required=False),
      # integer parameter 범위 지정을 위한 검증
        Param('is_selling', FORM, str, rules=[Pattern(r'^([0-1])$')]),
        Param('is_visible', FORM, str, rules=[Pattern(r'^([0-1])$')]),
        Param('sub_category_id', FORM, str,
              rules=[Pattern(r'^([0-9]|[0-9][0-9]|[1][0][0-9]|[1][1][0-4])$')]),
        Param('max_order', FORM, str,
              rules=[Pattern(r'^([1-9]|[1-2][0-9])$')]),
        Param('min_order', FORM, str,
              rules=[Pattern(r'^([1-9]|[1-2][0-9])$')])
              )
    def create_product(*args):
        connection = None

        # min_order, max_order 예외처리
        if args[16] > 20 or args[17] > 20:
            return jsonify({'message': 'ORDER_VALUE_ERROR'}), 400

        filter_data = {
            'editor_id'               : g.token_info['account_id'],
            'is_selling'              : args[0],
            'is_visible'              : args[1],
            'sub_category_id'         : args[2],
            'product_name'            : args[3],
            'is_information_notice'   : args[4],
            'manufacturer'            : args[5],
            'manufacture_date'        : args[6],
            'made_in'                 : args[7],
            'short_description'       : args[8],
            'is_inventory_management' : args[9],
            'inventory'               : args[10],
            'price'                   : args[11],
            'discount_rate'           : args[12],
            'is_discount_period'      : args[13],
            'discount_start_datetime' : args[14],
            'discount_end_datetime'   : args[15],
            'min_order'               : args[16],
            'max_order'               : args[17]
        }
        if args[18] :
            filter_data['seller_id'] = args[18]
        else:
            filter_data['seller_id'] = g.token_info['seller_id']

        print(filter_data['seller_id'])

        try:
            connection = connect_db()

            if connection:

                # option_list = '[{"name":"bb","age":29},{"name":"hh","age":20}]'
                options     = request.form.get('option_list')
                option_list = json.loads(options)

                #image 저장을 위한 S3 connection instance 생성
                """
                images : File Request(List)
                [
                    { 'product_image_<int>' : <FileStorage: {filename} ({content_type})>}
                ]
                """
                images = request.files
                image_bucket_dir = datetime.datetime.now().strftime('%Y-%m-%d')

                desc_image     = request.files.get('desc_image')
                desc_image_url = Image_uploader.upload_desc_images(desc_image,image_bucket_dir)

                filter_data['desc_img_url'] = desc_image_url

                product_service = ProductService()
                create_info     = product_service.create_product(filter_data, option_list, connection)

                product_id   = create_info['product_id']
                editor_id    = filter_data['editor_id']
                insert_count = create_info['create_count']

                #상품 이미지 URL화, S3에 올리기
                product_images = Image_uploader.upload_product_images(images,image_bucket_dir)

                #상품 이미지를 DB에 Insert하는 함수 실행
                product_service.upload_product_image(product_images, product_id, editor_id, connection)

                connection.commit()
                return jsonify({'message': f'{insert_count}products are created'}), 201
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except KeyError:
            connection.rollback()
            return jsonify({'message': 'KEY_ERROR'}), 400

        except Exception as e:
            connection.rollback()
            # raise e
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500


    @product_app.route('/download', methods=['GET'])
    @login_validator
    @validate_params(
        Param('started_date', GET, str, required=False,
              rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('ended_date', GET, str, required=False,
              rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('product_number', GET, str, required=False),
        Param('product_code', GET, str, required=False),
        Param('seller_subcategory_id', GET, list, required=False),
        Param('is_selling', GET, bool, rules=[Enum(0, 1)], required=False),
        Param('is_visible', GET, bool, rules=[Enum(0, 1)], required=False),
        Param('is_discount', GET, bool, rules=[Enum(0, 1)], required=False),
        Param('limit', GET, int, required=False),
        Param('page', GET, int, required=False)
    )
    def product_list_excel(*args):
        connection = None

        filter_data = {
            'started_date': args[0],
            'ended_date': args[1],
            'seller_name': args[2],
            'product_name': args[3],
            'product_number': args[4],
            'product_code': args[5],
            'seller_subcategory_id': args[6],
            'is_selling': args[7],
            'is_visible': args[8],
            'is_discount': args[9],
            'account_type_id': g.token_info['account_type_id'],
            'account_id' : g.token_info['account_id']
        }

        try:
            connection = connect_db()
            if connection:
                product_service = ProductService()

                product_service.product_excel(filter_data, connection)

                return jsonify({'message':'SUCCESS'}), 201
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 400

        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500


