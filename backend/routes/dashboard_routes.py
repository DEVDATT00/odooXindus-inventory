from flask import Blueprint, jsonify
from models import db, Product, Stock, Receipt

dashboard_routes = Blueprint("dashboard_routes", __name__)

@dashboard_routes.route("/summary", methods=["GET"])
def dashboard_stats():

    try:

        total_products = Product.query.count()

        total_stock = db.session.query(db.func.sum(Stock.quantity)).scalar() or 0

        low_stock_items = Stock.query.filter(Stock.quantity < 10).count()

        pending_receipts = Receipt.query.filter_by(status="Draft").count()

        return jsonify({
            "success": True,
            "total_products": total_products,
            "total_stock": total_stock,
            "low_stock_items": low_stock_items,
            "pending_receipts": pending_receipts
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500