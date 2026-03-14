from flask import Blueprint, request, jsonify
from database.db import get_connection

delivery_routes = Blueprint("delivery_routes", __name__)


# GET ALL DELIVERIES
@delivery_routes.route("/", methods=["GET"])
def get_deliveries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM deliveries ORDER BY id DESC")

    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    deliveries = []

    for row in rows:
        deliveries.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return jsonify(deliveries)


# GET SINGLE DELIVERY
@delivery_routes.route("/<int:id>", methods=["GET"])
def get_delivery(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM deliveries WHERE id=%s", (id,))
    columns = [col[0] for col in cursor.description]

    row = cursor.fetchone()
    delivery = dict(zip(columns, row)) if row else None

    cursor.execute("SELECT * FROM delivery_items WHERE delivery_id=%s", (id,))
    item_columns = [col[0] for col in cursor.description]

    items = []
    for r in cursor.fetchall():
        items.append(dict(zip(item_columns, r)))

    cursor.close()
    conn.close()

    return jsonify({
        "delivery": delivery,
        "items": items
    })


# CREATE DELIVERY
@delivery_routes.route("/create", methods=["POST"])
def create_delivery():

    data = request.json

    customer = data["customer"]
    items = data["items"]

    conn = get_connection()
    cursor = conn.cursor()

    # insert delivery
    cursor.execute(
        "INSERT INTO deliveries (customer, status) VALUES (%s,%s)",
        (customer, "draft")
    )

    delivery_id = cursor.lastrowid

    # insert delivery items
    for item in items:

        product_id = item["product_id"]
        warehouse_id = item["warehouse_id"]
        quantity = item["quantity"]

        cursor.execute(
            """
            INSERT INTO delivery_items
            (delivery_id, product_id, warehouse_id, quantity)
            VALUES (%s,%s,%s,%s)
            """,
            (
                delivery_id,
                product_id,
                warehouse_id,
                quantity
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Delivery created successfully",
        "delivery_id": delivery_id
    })