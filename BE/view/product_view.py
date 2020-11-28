from flask                   import request, Blueprint, jsonify, g
#from utils                   import login_validator
from service.product_service import ProductService
from db_connector            import connect_db
from flask_request_validator import (
    GET,
    FORM,
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
        Param('offset', GET, int, required=False),
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

        # 기간 정의
        started_date, ended_date = args[0], args[1]

        if started_date and ended_date:
            if ended_date < started_date:
                started_date = ended_date

        # 두 값이 안들어 왔을 경우 default
        if not started_date:
            started_date = '2016-05-24'
        if not ended_date:
            ended_date = '2025-05-24'

        seller_subcategory_id = args[6]

        # 상품을 등록하는 주체가 셀러이면, 자기 토큰을 이용해 본인 상품만 표출
        if args[13] != 1:
            account_id = 3
        else:
            account_id = args[14]
        # if auth_type_id != 1:
        #      account_id = g.account_info['account_id']

        #유효성 검사 완료한 쿼리 값 저장
        filter_data = {
            'started_date': started_date + ' 00:00:00',
            'ended_date': ended_date + ' 23:59:59',
            'seller_name': args[2],
            'product_name': args[3],
            'product_number': args[4],
            'product_code' : args[5],
            'seller_subcategory_id': seller_subcategory_id,
            'is_selling': args[7],
            'is_visible': args[8],
            'is_discount': args[9],
            'offset': args[10],
            'limit': args[11],
            'page' : args[12],
            'account_type_id' : args[13], # validator 완성 후 수정 예정
            'account_id' : account_id
        }

        # offset 과 limit 에 음수가 들어오면 default 값 지정
        # if filter_data['offset'] < 0:
        #     filter_data['offset'] = 0

        if filter_data['limit'] < 0:
            filter_data['limit'] = 10

        try:
            connection = connect_db()

            if connection:
                product_service = ProductService()
                products = product_service.get_product_list( filter_data, connection )
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
    ##@login_validator
    @validate_params(
        Param('account_type_id', GET, int, required=False),
        Param('seller_id', GET, int, required=False),
        Param('seller_name', GET, str, required=False))
    def get_main_category(*args):
        """ 상품 분류별 1차 카테고리 표출 엔드포인트
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
            filter_data = {
                'account_type_id': args[0],
                'seller_id' : args[1] ,
                'seller_name' : args[2]
            }
            print(filter_data)
            product_service = ProductService()
            products = product_service.product_main_category(filter_data, connection)

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 400
        else:
            return jsonify(products), 200
        finally:
            try:
                connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500



