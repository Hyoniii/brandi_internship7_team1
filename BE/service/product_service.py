from model.product_dao import ProductDao

class ProductService:
    # def get_first_categories(self,account_info,db_connection):
    #     """  상품 1차 카테고리 목록 표출
    #
    #     seller 마다 다른
    #     """

    def get_product_list(self, data, connection):
        product_dao = ProductDao()

        product_list = product_dao.product_list(data,connection)
        return product_list

