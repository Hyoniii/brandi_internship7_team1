class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao


    def get_product(self, conn):
        product_list = self.product_dao.what(conn)


