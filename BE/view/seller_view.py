from flask import (
    Blueprint,
    jsonify
)

from utils                  import login_validator
from db_connector           import connect_db
from service.seller_service import SellerService


class SellerView:

    seller_app = Blueprint('seller_app', __name__, url_prefix='/sellers')

    @seller_app.route('/home', methods=['GET'])
    @login_validator
    def seller_home():

        seller_service = SellerService()

        connection = None
        try:
            connection = connect_db()
            seller_summary = seller_service.get_seller_summary(connection)
            return jsonify(seller_summary), 200

        except Exception as e:
            return jsonify({"message": f'{e}'}), 400

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f'{e}'}), 500