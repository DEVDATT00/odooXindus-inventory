from flask import Blueprint, request, jsonify
from database.db import get_connection
import pymysql

receipt_routes = Blueprint("receipt_routes", __name__)


# -------------------------------------------------
# GET ALL RECEIPTS
# -------------------------------------------------
@receipt_routes.route("/", methods=["GET"])
def get_receipts():

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
    SELECT 
        r.id,
        r.supplier,
        r.status,
        r.created_at,
        COUNT(ri.id) AS items,
        SUM(ri.quantity) AS total_value
    FROM receipts r
    LEFT JOIN receipt_items ri ON r.id = ri.receipt_id
    GROUP BY r.id
    ORDER BY r.id DESC
    """)

    receipts = cursor.fetchall()

    conn.close()

    return jsonify(receipts)


# -------------------------------------------------
# GET SINGLE RECEIPT
# -------------------------------------------------
@receipt_routes.route("/<int:receipt_id>", methods=["GET"])
def get_receipt(receipt_id):

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM receipts WHERE id=%s",
        (receipt_id,)
    )

    receipt = cursor.fetchone()

    cursor.close()
    conn.close()

    if receipt:
        return jsonify(receipt)
    else:
        return jsonify({"error": "Receipt not found"}), 404


# -------------------------------------------------
# CREATE RECEIPT
# -------------------------------------------------
@receipt_routes.route("/create", methods=["POST"])
def create_receipt():

    data = request.json

    supplier = data["supplier"]
    items = data["items"]

    conn = get_connection()
    cursor = conn.cursor()

    # create receipt
    cursor.execute(
        "INSERT INTO receipts (supplier,status) VALUES (%s,%s)",
        (supplier, "Done")
    )

    receipt_id = cursor.lastrowid

    for item in items:

        product_id = item["product_id"]
        warehouse_id = item["warehouse_id"]
        quantity = int(item["quantity"])

        # insert receipt item
        cursor.execute("""
            INSERT INTO receipt_items
            (receipt_id,product_id,warehouse_id,quantity)
            VALUES(%s,%s,%s,%s)
        """, (receipt_id, product_id, warehouse_id, quantity))

        # ensure stock row exists
        cursor.execute("""
            INSERT INTO stock(product_id,warehouse_id,quantity)
            VALUES(%s,%s,0)
            ON DUPLICATE KEY UPDATE quantity = quantity
        """, (product_id, warehouse_id))

        # update stock
        cursor.execute("""
            UPDATE stock
            SET quantity = quantity + %s
            WHERE product_id=%s AND warehouse_id=%s
        """, (quantity, product_id, warehouse_id))

        # insert stock ledger
        cursor.execute("""
            INSERT INTO stock_ledger
            (product_id,warehouse_id,operation,quantity,reference_id)
            VALUES(%s,%s,'RECEIPT',%s,%s)
        """, (product_id, warehouse_id, quantity, receipt_id))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Receipt created",
        "receipt_id": receipt_id
    })