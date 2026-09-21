from typing import Optional

from domain.order import Order
from repository.database import place_an_order_db, connect_db, update_order_db,delete_order_db


def place_order(order : Order):
    customer_name = order.customer_name
    order_list = order.products_details
    all_product_ids = []
    products_id_list = list()
    unavailable_items_list = []
    remaining_quantities_list = []
    order_details = dict()
    if customer_name is None:
        return {"You must give a name!"}
    if order_list is None:
        return {"You must give a non empty list"}
    for item in order_list:
        if item.product_id is None:
            return {"You must give the product id!"}
        if item.quantity is None:
            return {"You must give the quantity of the product!"}
    for item in order_list:
        all_product_ids.append(item.product_id)
    for i in all_product_ids:
        if all_product_ids.count(i) > 1:
            return {"You can not order the same product separately!"}
    try:
        conn = connect_db()
        cursor = conn.cursor()
        item_details = []
        for item in order_list:
            sql_check_quantity = "SELECT product_availability,product_id FROM products WHERE product_id = %s"
            cursor.execute(sql_check_quantity, (item.product_id,))
            results = cursor.fetchone()
            if results is None:
                unavailable_items_list.append(f"There is no such a product with id : {item.product_id}!")
                continue
            product_availability = results[0]
            if product_availability <= 0 :
                unavailable_items_list.append(f"Product with id : {item.product_id} is not available!")
            if item.quantity <= 0:
                unavailable_items_list.append(f"You chose product with id : {item.product_id} but quantity <= 0!")
            if item.quantity > product_availability:
                unavailable_items_list.append(f"You chose product with id : {item.product_id} but you chose quantity = {item.quantity},whereas "
                                              f"product availability is {product_availability}!")
            if 0 < item.quantity <= product_availability:
                item_details.append(f"product with id : {item.product_id}")
                item_details.append(f"quantity ordered : {item.quantity}")
                order_details["products "] = item_details
                products_id_list.append(item.product_id)
                remaining_quantity = product_availability - item.quantity
                remaining_quantities_list.append(remaining_quantity)
        if unavailable_items_list:
            return {"Error ": "Order could not be placed", "Reasons ": f"{unavailable_items_list}"}
        order_id = place_an_order_db(customer_name, order_list)
        order_details["Order details, order id "] = order_id
        for i in range(len(order_list)):
            update_quantity_sql = "UPDATE products SET product_availability = %s WHERE product_id = %s"
            cursor.execute(update_quantity_sql,(remaining_quantities_list[i],products_id_list[i]))
        conn.commit()
        cursor.close()
        conn.close()
        return order_details
    except Exception as e:
        raise Exception(f"Error : {e}")

def update_order(order_id : int,changed_order : Order):
    try:
        updated_order_details = dict()
        unavailable_items_list = []
        remaining_quantities_list = []
        item_details = []
        inserted_new_products = []
        updated_new_products = []
        conn = connect_db()
        cursor = conn.cursor()
        sql_check_existence_id = "SELECT * FROM order_items WHERE order_id = %s"
        cursor.execute(sql_check_existence_id, (order_id,))
        results = cursor.fetchall()
        updated_order_details["Order with id "] = order_id
        if not results:
            return {f"This order with id = {order_id} does not exist!"}
        customer_name = changed_order.customer_name
        for order_item in changed_order.products_details:
            sql_check_quantity = "SELECT product_availability,product_id FROM products WHERE product_id = %s"
            cursor.execute(sql_check_quantity, (order_item.product_id,))
            results = cursor.fetchone()
            if results is None:
                unavailable_items_list.append(f"There is no such a product with id : {order_item.product_id}!")
                continue
            product_availability = results[0]
            if product_availability <= 0:
                unavailable_items_list.append(f"Product with id : {order_item.product_id} is not available!")
            if order_item.quantity <= 0:
                unavailable_items_list.append(f"You chose product with id : {order_item.product_id} but quantity <= 0!")
            if order_item.quantity > product_availability:
                unavailable_items_list.append(
                    f"You chose product with id : {order_item.product_id} but you chose quantity = {order_item.quantity},whereas "
                    f"product availability is {product_availability}!")
            if 0 < order_item.quantity <= product_availability:
                item_details.append(f"product with id : {order_item.product_id}")
                item_details.append(f"quantity ordered : {order_item.quantity}")
                updated_order_details["products "] = item_details
                remaining_quantity = product_availability - order_item.quantity
                remaining_quantities_list.append(remaining_quantity)
            if unavailable_items_list:
                return {"Error ": "Order could not be placed", "Reasons ": f"{unavailable_items_list}"}
            product_id = order_item.product_id
            quantity = order_item.quantity
            sql_check_item_id_in_this_order = "SELECT * FROM order_items WHERE order_id = %s AND product_id = %s"
            cursor.execute(sql_check_item_id_in_this_order, (order_id, product_id))
            temp_result = cursor.fetchone()
            if temp_result:
                updated_new_products.append(f"Product with id : {temp_result[2]}")
                updated_new_products.append(f"quantity ordered : {temp_result[3]}")
                update_order_db(order_id,temp_result[0],product_id,quantity,customer_name)
            else:
                inserted_new_products.append(order_item)
        updated_order_details["Products updated"] = updated_new_products
        if not updated_new_products:
            updated_order_details["Products updated"] = "None"
        if inserted_new_products:
            new_order = Order(
            customer_name = customer_name,
            products_details = inserted_new_products
            )
            place_order(new_order)
            updated_order_details["Inserted new products"] = inserted_new_products
        return updated_order_details
    except Exception as e:
        raise Exception(f"Error : {e}")

def delete_order(order_id : int):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql_check = "SELECT * FROM orders WHERE order_id = %s"
        cursor.execute(sql_check,(order_id,))
        results = cursor.fetchall()
        if results:
            delete_order_db(order_id)
            return {"message": f"Order with id {order_id} deleted successfully!"}
        else:
            return {"error": f"There is no such order with id {order_id} anymore!"}
    except Exception as e:
        raise Exception(f"Error : {e}")

