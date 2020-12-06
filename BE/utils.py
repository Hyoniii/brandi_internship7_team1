import os, io, jwt, uuid
import pymysql

from PIL          import Image
from flask        import request, jsonify, g
from db_connector import connect_db, get_s3_connection
from mysql.connector.errors import Error
from config       import SECRET_KEY, ALGORITHM


def login_validator(func):

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
                                    'seller_id'       : None}
                                return func(*args, **kwargs)
                            return jsonify({'MESSAGE' : 'account_not_active'}), 400
                        return jsonify({'MESSAGE' : 'account_nonexistant'}), 404

                    except Error as e:
                        return Jsonify({'MESSAGE' : 'DB_error'}), 400

            except jwt.InvalidTokenError:
                return jsonify({'MESSAGE' : 'invalid_token'}), 401

            return jsonify({'MESSAGE' : 'no_db_connection'}), 400
        return jsonify({'MESSAGE' : 'invalid_token'}), 401
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




