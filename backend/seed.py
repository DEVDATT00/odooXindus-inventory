from app import db
from models import Product, Stock, Receipt

def seed_data():
    # Skip if products already exist (to avoid duplicates)
    if Product.query.count() > 0:
        print("Products already exist → skipping seed (you can comment this check if you want to re-seed)")
        return

    print("Starting to seed data...")

    # Create sample products
    products = [
        Product(name="Wireless Mouse Logitech M185", sku="PROD-001", category="Electronics", cost_price=450, sell_price=799),
        Product(name="USB-C Cable 2m", sku="PROD-002", category="Accessories", cost_price=180, sell_price=249),
        Product(name="Laptop Stand", sku="PROD-003", category="Peripherals", cost_price=1200, sell_price=1450),
        Product(name="HDMI Cable", sku="PROD-004", category="Electronics", cost_price=320, sell_price=380),
        Product(name="External SSD 1TB", sku="PROD-005", category="Electronics", cost_price=5200, sell_price=6200),
    ]
    db.session.add_all(products)
    db.session.commit()

    print(f"Added {len(products)} products.")

    # Add stock entries (warehouse removed because it's not in the Stock model anymore)
    for p in products:
        # Main warehouse stock
        db.session.add(Stock(
            product_id=p.id,
            quantity=142 if p.sku == "PROD-001" else
                     89 if p.sku == "PROD-002" else
                     34 if p.sku == "PROD-003" else
                     211 if p.sku == "PROD-004" else 18
        ))
        
        # Store B stock (only for some products)
        if p.sku in ["PROD-001", "PROD-003"]:
            db.session.add(Stock(
                product_id=p.id,
                quantity=28 if p.sku == "PROD-001" else 15
            ))

    # Receipts (uncomment if you want to add them)
    # db.session.add(Receipt(reference="PO-2026-0456", supplier="Tech Distributors", status="pending"))
    # db.session.add(Receipt(reference="PO-2026-0457", supplier="Global Gadgets", status="received"))

    db.session.commit()

    print("✅ Dashboard seed data created!")
    print(f"Total products: {Product.query.count()}")
    print(f"Total stock entries: {Stock.query.count()}")