import pymysql
import time
import schedule

from pymysql import ProgrammingError
from model import OrderDao
from db_connector import connect_db


def confirm_order():
    connection = None
    order_dao = OrderDao()
    try:
        connection = connect_db()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                order_items.id,
                order_items.detailed_order_number
            FROM order_items
            INNER JOIN order_logs 
            ON (order_logs.order_item_id = order_items.id AND order_logs.order_status_id = order_items.order_status_id)
            WHERE order_items.order_status_id = 4
            AND order_logs.created_at < (CURRENT_TIMESTAMP() - INTERVAL 2 MINUTE)
            """
            cursor.execute(query)
            orders = cursor.fetchall()

            order_item_id = [order['id'] for order in orders]

            confirm_order = {
                "order_item_id": order_item_id,
                "order_status_id": 4,
                "new_order_status_id": 5
            }
            confirmed_orders = order_dao.update_order_status(connection, confirm_order)

            order_log = [
                [order['id'], None, 5]
                for order in orders
            ]
            created_logs = order_dao.create_order_log(connection, order_log)

            if len(orders) == confirmed_orders == created_logs:
                connection.commit()
                for order in orders:
                    print(f"Order confirmed: no.{order['detailed_order_number']}")
            else:
                connection.rollback()
                print("Something went wrong with order confirmation. Will try again in 1 minute")

    except ProgrammingError:
        connection.rollback()
        print("No order to update. Will try again in 1 minute")

    finally:
        try:
            if connection:
                connection.close()
        except Exception as e:
            print(f"connection error: {e}")


def run_scheduler():
    schedule.every(30).seconds.do(confirm_order)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
