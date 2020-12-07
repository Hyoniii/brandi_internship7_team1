import pymysql, boto3
import boto3
from config import DATABASE
from config import S3

def connect_db():
    db = pymysql.connect(
                            host     = DATABASE['host'],
                            port     = DATABASE['port'],
                            user     = DATABASE['user'],
                            password = DATABASE['password'],
                            database = DATABASE['database'],
                            charset  = DATABASE['charset'],
                            #cursor   = pymysql.cursors.DictCursor,
                            autocommit = False,
                            read_timeout = 20,
                            db = 'brandi',
                            )
    return db


def get_s3_connection():
    s3_connection = boto3.client(
        's3',
        aws_access_key_id     = S3['aws_access_key_id'],
        aws_secret_access_key = S3['aws_secret_access_key']
    )

    return s3_connection