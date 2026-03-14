from flask import Flask
from flask_cors import CORS
from models import db

from routes.auth_routes import auth_routes
from routes.product_routes import product_routes
from routes.receipt_routes import receipt_routes
from routes.delivery_routes import delivery_routes
from routes.dashboard_routes import dashboard_routes
from routes.adjustment_routes import adjustment_routes

app = Flask(__name__)
CORS(app)

# MySQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/inventory_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect SQLAlchemy with Flask
db.init_app(app)

# Register routes
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(product_routes, url_prefix="/api/products")
app.register_blueprint(receipt_routes, url_prefix="/api/receipts")
app.register_blueprint(delivery_routes, url_prefix="/api/deliveries")
app.register_blueprint(dashboard_routes, url_prefix="/api/dashboard")
app.register_blueprint(adjustment_routes, url_prefix="/api/adjustments")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)