from flask                   import request, Blueprint, jsonify, g
#from utils                   import login_validator
from service.product_service import ProductService
from db_connector            import connect_db
from flask_request_validator import (
    GET,
    FORM,
    JSON,
    PATH,
    Param,
    Pattern,
    validate_params
)



class ProductView:
    product_app = Blueprint('product_app', __name__, url_prefix='/products')

    @product_app.route('', methods=['GET'])
    ##@login_validator
    @validate_params(
        Param('started_date', GET, str, required=False,
              rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('ended_date', GET, str, required=False,
              rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('product_number', GET, int, required=False),
        Param('product_code', GET, str, required=False),
        Param('seller_subcategory_id', GET, list, required=False),
        Param('is_selling', GET, bool, required=False),
        Param('is_visible', GET, bool, required=False),
        Param('is_discount', GET, bool, required=False),
        Param('limit', GET, int, required=False),
        Param('page', GET, int, required=False),
        Param('account_type_id', GET, int, required=False),#login_validator 완성 후 삭제 예정
        Param('account_id', GET, int, required=False),  # login_validator 완성 후 삭제 예정
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
        # 상품을 등록하는 주체가 셀러이면, 자기 토큰을 이용해 본인 상품만 표출
        if args[13] != 1:
            account_id = 3
        else:
            account_id = args[14]
        # if auth_type_id != 1:
        #      account_id = g.account_info['account_id']

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
            'account_type_id'       : args[12], # validator 완성 후 수정 예정
            'account_id'            : account_id
        }

        try:
            connection = connect_db()

            if connection:
                product_service = ProductService()
                products        = product_service.get_product_list( filter_data, connection )
                return jsonify({'data':products}),200
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
    ##@login_validator
    @validate_params(
        Param('account_type_id', GET, int, required=False),
        Param('seller_id', GET, int, required=False),
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
            500: server error

        History:
            2020-11-30 : 초기 생성
        """
        connection = None
        try:
            connection = connect_db()
            if connection:
                filter_data = {
                    'account_type_id': args[0],
                    'seller_id'      : args[1] ,
                    'seller_name'    : args[2]
                }

                product_service = ProductService()
                main_categories_data = product_service.product_main_category(filter_data, connection)
        except Exception as e:
            return jsonify({'message' : f'{e}'}), 400
        else:
            return jsonify({'data':main_categories_data}), 200
        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/category/<int:main_category_id>', methods=['GET'])
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
    ##@login_validator
    @validate_params(
        Param('is_selling', JSON, int),
        Param('is_visible', JSON, int),
        Param('sub_category_id', JSON, int, required=False),
        Param('product_name', JSON, str,
              rules=[Pattern(r"[^\"\']")]),
        Param('is_information_notice', JSON, int),
        Param('manufacturer', JSON, str, required=False),
        Param('manufacture_date', JSON, str, required=False, rules=[Pattern(r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$")]),
        Param('made_in', JSON, str, required=False),
        Param('short_description', JSON, str, required=False),
        Param('is_inventory_management', JSON, int),
        Param('inventory', JSON, int, required=False),
        Param('price', JSON, int),
        Param('discount_rate', JSON, float, required=False),
        Param('is_discount_period', JSON, int),
        Param('discount_start_time', JSON, str, required=False),
        Param('discount_end_time', JSON, str, required=False),
        Param('min_order', JSON, int),
        Param('max_order', JSON, int),
        Param('seller_id', JSON, int, required=False),
        Param('option_list', JSON, list),
      # integer parameter 범위 지정을 위한 검증
        Param('is_selling', JSON, str,
              rules=[Pattern(r'^([0-1])$')]),
        Param('is_visible', JSON, str,
              rules=[Pattern(r'^([0-1])$')]),
        Param('sub_category_id', JSON, str,
              rules=[Pattern(r'^([0-9]|[0-9][0-9]|[1][0][0-9]|[1][1][0-4])$')]),
        Param('max_order', JSON, str,
              rules=[Pattern(r'^([1-9]|[1-2][0-9])$')]),
        Param('min_order', JSON, str,
              rules=[Pattern(r'^([1-9]|[1-2][0-9])$')])
              )
    def create_product(*args):
        connection = None

        if args[16] > 19 or args[17] > 19:
            return jsonify({'message': 'value_error'}), 400

        filter_data = {
            'editor_id'               : 2, #디버깅용 하드코딩,g.account['account_id']
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
            'max_order'               : args[17],
            'seller_id'               : args[18], #if args[20] else g.token_info['seller_id'],
            'desc_img_url'            : "image.jpg",
            'option_list'             : args[19]
        }
        try:
            connection = connect_db()

            if connection:
                product_service = ProductService()
                product_service.create_product(filter_data, connection)
                connection.commit()
                return jsonify({'message' : 'SUCCESS'}), 200
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            connection.rollback()
            return jsonify({'message': f'{e}'}), 500

        except KeyError:
            db_connection.rollback()
            return jsonify({'message' 'KEY_ERROR'}), 400

        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500



