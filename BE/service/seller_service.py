from flask import g

from model.seller_dao import SellerDao


class SellerService():

    def __init__(self):
        pass

    def get_seller_summary(self, connection):

        seller_dao = SellerDao()

        seller_id = g.token_info['seller_id']
        products = seller_dao.count_seller_products(connection, seller_id)

        return products

