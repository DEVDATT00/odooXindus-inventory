from flask import Blueprint, request, jsonify
from database.db import get_connection

receipt_routes = Blueprint("receipt_routes", __name__)

# LIST RECEIPTS
@receipt_routes.route("/", methods=["GET"])
def get_receipts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receipts")
    receipts = cursor.fetchall()

    return jsonify(receipts)


# CREATE RECEIPT
@receipt_routes.route("/create", methods=["POST"])
def create_receipt():

    data = request.json
    supplier = data["supplier"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO receipts(supplier) VALUES(%s)",
        (supplier,)
    )

    conn.commit()

    return jsonify({"message":"Receipt created"})