import os, io, jwt, uuid
import pymysql
import xlsxwriter
import time
import datetime

from functools    import wraps
from PIL          import Image
from flask        import request, jsonify, g, send_file

from db_connector import connect_db, get_s3_connection
from mysql.connector.errors import Error
from config       import SECRET_KEY, ALGORITHM


def login_validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('AUTHORIZATION', None)

        if access_token:
            try:

                payload    = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                account_id = payload['account_id']
                connection = connect_db()

                if connection:
                    try:
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            query = """
                                SELECT
                                    accounts.account_type_id,
                                    accounts.is_active,
                                    accounts.id,
                                    sellers.id as seller_id
                                FROM
                                    accounts
                                LEFT JOIN
                                    sellers ON sellers.account_id = accounts.id
                                WHERE
                                    accounts.id = %(account_id)s
                            """
                            cursor.execute(query, {'account_id': account_id})
                            account = cursor.fetchone()
                        if account:
                            if account['is_active'] == 1:
                                g.token_info = {
                                    'account_id'      : account_id,
                                    'account_type_id' : account['account_type_id'],
                                    'seller_id'       : account['seller_id']}
                                return func(*args, **kwargs)
                            return jsonify({'MESSAGE': 'account_not_active'}), 400
                        return jsonify({'MESSAGE': 'account_nonexistant'}), 404

                    except Error as e:
                        return Jsonify({'MESSAGE': 'DB_error'}), 400

            except jwt.InvalidTokenError:
                return jsonify({'MESSAGE': 'invalid_token'}), 401

            return jsonify({'MESSAGE': 'no_db_connection'}), 400
        return jsonify({'MESSAGE': 'invalid_token'}), 401
    return wrapper


class Image_uploader:
    def __init__(self):
        pass

    def upload_desc_images(desc_images):

        s3_connection = None

        try:
            s3_connection = get_s3_connection()

            if desc_images:
                image = Image.open(desc_images)
                width, height = image.size

                if width < 1000:
                    image = Image.new("RGB", (1000, height))

                buffer = io.BytesIO()
                image.save(buffer, "JPEG")
                buffer.seek(0)

                filename = str(uuid.uuid1()).replace('-', '')

                try:
                    s3_connection.put_object(
                        Body        = buffer,
                        Bucket      = 'brandi-intern01',
                        Key         = filename,
                        ContentType = 'image/jpeg'
                    )

                except KeyError as e:
                    raise e

                except Exception as e:
                    raise e

                image_url = f'https://brandi-intern01.s3.ap-northeast-2.amazonaws.com/{filename}'


        except KeyError as e:
            raise e

        except Exception as e:
            raise e

        return image_url


    def upload_product_images(images):

        s3_connection = get_s3_connection()

        product_images = []

        try:
            for num in range(1, 6):

                # 대표사진 미등록 예외처리
                if 'product_image_1' not in images:
                    raise Exception('THUMBNAIL_IMAGE_IS_REQUIRED')

                # 상품사진 미정렬 예외처리
                if num > 2:
                    if (f'product_image_{num}' in images) and (f'product_image_{num - 1}' not in images):
                        raise Exception('IMAGE_CAN_ONLY_REGISTER_IN_ORDER')

                # 상품사진 있는 경우 product_images Dictionary에 저장
                if images.get(f'product_image_{num}'):
                    # 파일이 Image가 아닌 경우 Exception 발생
                    image         = Image.open(images[f'product_image_{num}'])
                    width, height = image.size

                    # 사이즈가 너무 작은 경우 예외처리
                    if width < 640 or height < 720:
                        image = Image.new("RGB", (640,720))
                        #raise Exception('IMAGE_SIZE_IS_TOO_SMALL')

                    buffer = io.BytesIO()
                    image.save(buffer, "JPEG")
                    buffer.seek(0)

                    filename = f'product_image_{num}'

                    try:
                        s3_connection.put_object(
                            Body        = buffer,
                            Bucket      ='brandi-intern01',
                            Key         = filename,
                            ContentType ='image/jpeg'
                        )

                    except KeyError as e:
                        raise e
                    except Exception as e:
                        raise e

                    image_url = f'https://brandi-intern01.s3.ap-northeast-2.amazonaws.com/{filename}'
                    product_images.append({'image_url': image_url})

            return product_images

        except Exception as e:
            raise e




class Product_excel_downloader:
    def __init__(self):
        pass

    def master_product_excel_down(excel_info):
        null = 0
        for data in excel_info:

            if data['is_selling'] == 1:
                data['is_selling'] = "판매"
            else:
                data['is_selling'] = "미판매"

            if data['is_visible'] == 1:
                data['is_visible'] = "진열"
            else:
                data['is_visible'] = "미진열"

            if data['is_discount'] == 1:
                data['is_discount'] = "할인"
            else:
                data['is_discount'] = "미할인"

            data['price'] = int(data['price'])

            data['created_at'] = data['created_at'].strftime('%Y-%m-%d')

            if data.get('discount_price') is None:
                data['discount_price'] = data['price']


        workbook = xlsxwriter.Workbook('master_product_list.xlsx')
        worksheet = workbook.add_worksheet()

        # file = io.BytesIO()
        # wb.save(file)
        # file.seek(0)

        columns = ['등록일', '대표이미지', '상품명', '상품코드', '상품번호', '셀러속성', '셀러명', '판매가', '할인가', '판매여부', '진열여부', '할인여부']

        for column in columns:
            worksheet.write(0, columns.index(column), column)

        row = 1
        col = 0
        #######datetile#############
        for j in excel_info:
            worksheet.write(row, col,     j.get('created_at'))
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

        workbook.close()
        return send_file('master_product_list.xlsx')


    def seller_product_excel_down(excel_info):
        null = 0
        for data in excel_info:

            if data['is_selling'] == 1:
                data['is_selling'] = "판매"
            else:
                data['is_selling'] = "미판매"

            if data['is_visible'] == 1:
                data['is_visible'] = "진열"
            else:
                data['is_visible'] = "미진열"

            if data['is_discount'] == 1:
                data['is_discount'] = "할인"
            else:
                data['is_discount'] = "미할인"

            data['price'] = int(data['price'])

            data['created_at'] = data['created_at'].strftime('%Y-%m-%d')

            if data.get('discount_price') is None:
                data['discount_price'] = data['price']

        workbook = xlsxwriter.Workbook('seller_product_list.xlsx')
        worksheet = workbook.add_worksheet()

        columns = ['등록일', '대표이미지', '상품명', '상품코드', '상품번호', '판매가', '할인가', '판매여부', '진열여부', '할인여부']

        for column in columns:
            worksheet.write(0, columns.index(column), column)

        row = 1
        col = 0

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
        return send_file('seller_product_list.xlsx')





