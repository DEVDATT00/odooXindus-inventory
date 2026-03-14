from flask import Blueprint, request, jsonify
from models import db, Product, Category, Stock
from sqlalchemy import func

product_routes = Blueprint("product_routes", __name__)

# =========================
# GET ALL PRODUCTS
# =========================
@product_routes.route("/", methods=["GET"])
def get_products():

    products = (
        db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            Product.unit,
            Category.name.label("category"),
            func.coalesce(func.sum(Stock.quantity), 0).label("stock")
        )
        .outerjoin(Category, Product.category_id == Category.id)
        .outerjoin(Stock, Product.id == Stock.product_id)
        .group_by(Product.id, Product.name, Product.sku, Product.unit, Category.name)
        .all()
    )

    data = []

    for p in products:

        qty = p.stock

        if qty == 0:
            status = "out"
        elif qty < 20:
            status = "low"
        else:
            status = "instock"

        data.append({
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "unit": p.unit,
            "category": p.category,
            "stock": qty,
            "status": status
        })

    return jsonify(data)


# =========================
# ADD PRODUCT
# =========================
@product_routes.route("/", methods=["POST"])
def add_product():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    product = Product(
        name=data["name"],
        sku=data["sku"],
        category_id=data["category_id"],
        unit=data["unit"],
        stocklevel=data.get("stocklevel", 0)
    )

    db.session.add(product)
    db.session.flush()  # get product.id before commit

    # create stock entry automatically
    stock = Stock(
        product_id=product.id,
        warehouse_id=1,
        quantity=0
    )

    db.session.add(stock)
    db.session.commit()

    return jsonify({"success": True})


# =========================
# GET SINGLE PRODUCT
# =========================
@product_routes.route("/<int:id>", methods=["GET"])
def get_product(id):

    p = Product.query.get_or_404(id)

    return jsonify({
        "id": p.id,
        "name": p.name,
        "sku": p.sku,
        "category_id": p.category_id,
        "unit": p.unit,
        "stocklevel": p.stocklevel
    })


# =========================
# UPDATE PRODUCT
# =========================
@product_routes.route("/<int:id>", methods=["PUT"])
def update_product(id):

    p = Product.query.get_or_404(id)

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    p.name = data["name"]
    p.sku = data["sku"]
    p.category_id = data["category_id"]
    p.unit = data["unit"]
    p.stocklevel = data.get("stocklevel", p.stocklevel)

    db.session.commit()

    return jsonify({"success": True})


# =========================
# DELETE PRODUCT
# =========================
@product_routes.route("/<int:id>", methods=["DELETE"])
def delete_product(id):

    product = Product.query.get_or_404(id)

    # delete stock first because of foreign key
    Stock.query.filter_by(product_id=id).delete(synchronize_session=False)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"success": True})