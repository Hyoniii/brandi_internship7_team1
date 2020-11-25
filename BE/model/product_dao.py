import pymysql

class ProductDao:
    def what(self, conn):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # query = """
            # SELECT ...
            # """
            #
            # products = cursor.execute(query)
            #
            # return cursor.fetchall()

            print('1')
            return '1'
    def art():
        print('2')
    def thou():
        print('3')