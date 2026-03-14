-- =====================================
-- INVENTORY MANAGEMENT SYSTEM DATABASE
-- =====================================

CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

-- =====================================
-- USERS TABLE
-- =====================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('manager','staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- PRODUCT CATEGORIES
-- =====================================

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- =====================================
-- PRODUCTS
-- =====================================

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    category_id INT,
    unit VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- =====================================
-- WAREHOUSES
-- =====================================

CREATE TABLE warehouses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200)
);

-- =====================================
-- STOCK TABLE
-- =====================================

CREATE TABLE stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- =====================================
-- RECEIPTS (INCOMING GOODS)
-- =====================================

CREATE TABLE receipts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier VARCHAR(200),
    status ENUM('Draft','Done') DEFAULT 'Draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- RECEIPT ITEMS
-- =====================================

CREATE TABLE receipt_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_id INT,
    product_id INT,
    warehouse_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (receipt_id) REFERENCES receipts(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- =====================================
-- DELIVERIES (OUTGOING GOODS)
-- =====================================

CREATE TABLE deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer VARCHAR(200),
    status ENUM('Draft','Done') DEFAULT 'Draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- DELIVERY ITEMS
-- =====================================

CREATE TABLE delivery_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    delivery_id INT,
    product_id INT,
    warehouse_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- =====================================
-- INTERNAL TRANSFERS
-- =====================================

CREATE TABLE transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    from_warehouse INT,
    to_warehouse INT,
    quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- =====================================
-- STOCK LEDGER (MOVEMENT HISTORY)
-- =====================================

CREATE TABLE stock_ledger (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    operation VARCHAR(50),
    quantity INT,
    reference_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- SAMPLE DATA
-- =====================================

INSERT INTO categories (name) VALUES
('Raw Material'),
('Finished Goods');

INSERT INTO warehouses (name, location) VALUES
('Main Warehouse','Building A'),
('Production Floor','Building B');

INSERT INTO users (name,email,password,role) VALUES
('Admin','admin@test.com','admin123','manager');