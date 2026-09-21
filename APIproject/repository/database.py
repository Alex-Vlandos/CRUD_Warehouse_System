from typing import Optional,List

import psycopg2

from domain.order import OrderItem, Order
from domain.product import Product


def connect_db():
    db_config = {
        "dbname" : "students",
        "user" : "postgres",
        "password" : "pass123",
        "host" : "localhost",
        "port" : "5432"
    }

    connection = psycopg2.connect(**db_config)
    return connection

def create_product_db(name,desc,price,availability):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products(product_name,product_description,product_price,product_availability) "
                                "VALUES(%s,%s,%s,%s)",(name,desc,price,availability))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception("Unsuccessful creation!")

def get_products_details_db():
    try:
        products_dict = dict()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        results = cursor.fetchall()
        products_dict["Available products list"] = []
        for result in results:
            product_dict_temp = dict()
            product_dict_temp["product id"] = result[0]
            product_dict_temp["product name"] = result[1]
            product_dict_temp["product description"] = result[2]
            product_dict_temp["product price"] = result[3]
            product_dict_temp["product quantity"] = result[4]
            products_dict["Available products list"].append(product_dict_temp)
        cursor.close()
        conn.close()
        return products_dict
    except Exception as e:
        raise Exception("Error")

def update_product_db(product_id,name = None,desc = None,price = None,availability = None):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        keys = []
        values = []

        if name is not None:
            keys.append("product_name = %s")
            values.append(name)
        if desc is not None:
            keys.append("product_description = %s")
            values.append(desc)
        if price is not None:
            keys.append("product_price = %s")
            values.append(price)
        if availability is not None:
            keys.append("product_availability = %s")
            values.append(availability)
        if not keys:
            raise Exception("Message : None field given for update!")
        values.append(product_id)
        sql_query = f"UPDATE products SET {', '.join(keys)} WHERE product_id = %s"

        cursor.execute(sql_query,values)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Error {e}")
def delete_product_db(product_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products "
                                      "WHERE product_id = %s",(product_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Error:{e}")

def search_products_db(name : Optional[str]=None,min_price:Optional[float]=None,max_price:Optional[float]=None,min_quantity:Optional[int]=None,max_quantity:Optional[int]=None):
    sql = "SELECT * from products WHERE true "
    parameters = []

    if name is not None:
        sql += f"AND product_name LIKE %s "
        parameters.append(f"%{name}%")
    if min_price is not None and max_price is None:
        sql += f"AND product_price >= %s "
        parameters.append(f"{min_price}")
    if max_price is not None and min_price is None:
        sql += f"AND product_price <= %s "
        parameters.append(f"{max_price}")
    if min_price is not None and max_price is not None:
        sql += f"AND product_price BETWEEN %s AND %s "
        parameters.append(f"{min_price}")
        parameters.append(f"{max_price}")
    if min_quantity is not None and max_quantity is None:
        sql += f"AND product_availability >= {min_quantity} "
        parameters.append(f"{min_quantity}")
    if max_quantity is not None and min_quantity is None:
        sql += f"AND product_availability <= {max_quantity} "
        parameters.append(f"{max_quantity}")
    if min_quantity is not None and max_quantity is not None:
        sql += f"AND product_availability BETWEEN %s AND %s "
        parameters.append(f"{min_quantity}")
        parameters.append(f"{max_quantity}")
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(sql,tuple(parameters))
        results = cursor.fetchall()
        products_dict = dict()
        products_dict["Available products list"] = []
        for result in results:
            product_dict_temp = dict()
            product_dict_temp["product id"] = result[0]
            product_dict_temp["product name"] = result[1]
            product_dict_temp["product description"] = result[2]
            product_dict_temp["product price"] = result[3]
            product_dict_temp["product quantity"] = result[4]
            products_dict["Available products list"].append(product_dict_temp)
        cursor.close()
        conn.close()
        return products_dict
    except Exception as e:
        raise Exception(f"Error:{e}")

def place_an_order_db(customer_name : str,products_details : List[OrderItem]):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql_order_table = "INSERT INTO orders(customer_name) VALUES (%s) RETURNING order_id "
        cursor.execute(sql_order_table,(customer_name,))
        order_id = cursor.fetchone()[0]
        for item in products_details:
            sql = "INSERT INTO order_items(order_id,product_id,quantity) VALUES (%s,%s,%s) "
            cursor.execute(sql, (order_id, item.product_id, item.quantity))
        conn.commit()
        cursor.close()
        conn.close()
        return order_id
    except Exception as e:
        raise Exception(f"Error : {e}")


def update_order_db(order_id : int,order_item_id : int,new_product_id : Optional[int]=None,new_quantity : Optional[int]=None,customer_name : Optional[str]=None):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        keys = []
        values = []
        message = dict()
        message["order id"] = order_id
        message["order item id"] = order_item_id
        if new_product_id is None and new_quantity is None:
            return {"You must choose a new quantity or a new product or both fields!"}
        if new_product_id is not None:
            keys.append("product_id = %s")
            values.append(new_product_id)
            message["new product id"] = new_product_id
        if new_quantity is not None:
            keys.append("quantity = %s")
            values.append(new_quantity)
            message["new quantity"] = new_quantity
        if customer_name is not None:
            sql_order_table_update = "UPDATE orders SET customer_name = %s WHERE order_id = %s"
            cursor.execute(sql_order_table_update,(customer_name,order_id))
            message["new customer name"] = customer_name
        values.append(order_item_id)
        values.append(order_id)
        sql_update = f"UPDATE order_items SET {','.join(keys)} WHERE order_item_id = %s AND order_id = %s"
        cursor.execute(sql_update,tuple(values))
        conn.commit()
        cursor.close()
        conn.close()
        return message
    except Exception as e:
        raise Exception(f"Error {e}")

def delete_order_db(order_id : int):
    try:
        conn = connect_db()
        cursor =conn.cursor()
        sql_delete_order = "DELETE FROM orders WHERE order_id = %s"
        cursor.execute(sql_delete_order,(order_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Error : {e}")

def products_statistics_db():
    try:
        message = dict()
        conn = connect_db()
        cursor =conn.cursor()
        cursor.execute("SELECT COUNT(product_id),SUM(product_availability),AVG(product_price) FROM products")
        statistics = cursor.fetchone()
        message["total_amount_of_different_products"] = statistics[0]
        message["total_stock"] = statistics[1]
        message["average_total_price"] = statistics[2]
        cursor.execute("SELECT * FROM products ORDER BY product_price DESC")
        results1 = cursor.fetchall()
        message["products_descending_price"] = []
        message["products_ascending_price"] = []
        for result in results1:
            product_info = {
                "product_id": result[0],
                "product_name": result[1],
                "product_description": result[2],
                "product_price": result[3],
                "product_availability": result[4]
            }
            message["products_descending_price"].append(product_info)
        cursor.execute("SELECT * FROM products ORDER BY product_price ASC")
        results2 = cursor.fetchall()
        for result in results2:
            product_info = {
                "product_id": result[0],
                "product_name": result[1],
                "product_description": result[2],
                "product_price": result[3],
                "product_availability": result[4]
            }
            message["products_ascending_price"].append(product_info)
        return message
    except Exception as e:
        raise Exception(f"Error : {e}")
