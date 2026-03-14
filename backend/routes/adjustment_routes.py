from flask import Blueprint, request, jsonify
from database.db import get_connection

adjustment_routes = Blueprint("adjustment_routes", __name__)

@adjustment_routes.route("/adjust", methods=["POST"])
def adjust_stock():

    data = request.json

    product_id = data["product_id"]
    warehouse_id = data["warehouse_id"]
    quantity = int(data["quantity"])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    UPDATE stock
    SET quantity = quantity + %s
    WHERE product_id=%s AND warehouse_id=%s
    """,
    (quantity,product_id,warehouse_id)
    )

    cursor.execute(
    """
    INSERT INTO stock_ledger
    (product_id,warehouse_id,operation,quantity,reference_id)
    VALUES(%s,%s,'ADJUSTMENT',%s,0)
    """,
    (product_id,warehouse_id,quantity)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message":"Stock adjusted"})