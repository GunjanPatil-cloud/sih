-- SIH Packaged Commodity Compliance Prototype
-- 50-product seed dataset
-- IMPORTANT: This is prototype seed data. Verify barcode, FSSAI licence,
-- ingredients, nutrition, MRP and batch/date information from the actual package
-- before presenting the data as real-world regulatory evidence.

CREATE DATABASE IF NOT EXISTS sih_compliance;
USE sih_compliance;

DROP TABLE IF EXISTS product_batches;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    standard_pack_size VARCHAR(50),
    barcode VARCHAR(50) UNIQUE NULL,
    manufacturer VARCHAR(255) NULL,
    ingredients TEXT NULL,
    allergens TEXT NULL,
    veg_nonveg VARCHAR(20) NULL,
    fssai_license_no VARCHAR(100) NULL,
    country_of_origin VARCHAR(100) DEFAULT 'India',
    customer_care_details VARCHAR(255) NULL,
    package_type VARCHAR(100) NULL,
    source_status VARCHAR(50) NOT NULL DEFAULT 'DEMO_VERIFY',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_batches (
    batch_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    batch_no VARCHAR(100) NULL,
    mrp DECIMAL(10,2) NULL,
    manufacturing_date DATE NULL,
    expiry_date DATE NULL,
    net_quantity VARCHAR(50) NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Maggi 2-Minute Masala Noodles', 'Nestlé', 'Instant Noodles', '70 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Parle-G Original Glucose Biscuits', 'Parle Products', 'Biscuits', '800 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Britannia Good Day Butter Cookies', 'Britannia', 'Biscuits', '200 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Lay''s Classic Salted', 'Lay''s', 'Potato Chips', '50 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Coca-Cola Original Taste', 'Coca-Cola', 'Carbonated Beverage', '750 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Jim Jam Cream Biscuit', 'Parle Products', 'Biscuits', '150 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Kurkure Masala Munch', 'Kurkure', 'Extruded Snack', '90 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Lay''s Magic Masala', 'Lay''s', 'Potato Chips', '50 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Britannia Good Day Cashew', 'Britannia', 'Biscuits', '200 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Sprite Lemon-Lime', 'Sprite', 'Carbonated Beverage', '750 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Red Bull Energy Drink', 'Red Bull', 'Energy Drink', '250 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Monster Energy Original', 'Monster', 'Energy Drink', '350 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Diet Coke', 'Coca-Cola', 'Carbonated Beverage', '300 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Center Fresh Mint', 'Center Fresh', 'Chewing Gum', '25.92 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Happydent White', 'Happydent', 'Chewing Gum', '28 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Britannia Marie Gold', 'Britannia', 'Biscuits', '250 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Britannia Bourbon', 'Britannia', 'Biscuits', '150 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Parle Hide & Seek', 'Parle Products', 'Biscuits', '120 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Parle KrackJack', 'Parle Products', 'Biscuits', '200 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Sunfeast Dark Fantasy', 'Sunfeast', 'Biscuits', '300 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Sunfeast Marie Light', 'Sunfeast', 'Biscuits', '250 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Oreo Original', 'Oreo', 'Biscuits', '120 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Too Yumm! Karare', 'Too Yumm!', 'Snacks', '60 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Haldiram''s Aloo Bhujia', 'Haldiram''s', 'Namkeen', '200 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Bingo! Tedhe Medhe', 'Bingo!', 'Snacks', '90 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Bingo! Mad Angles', 'Bingo!', 'Snacks', '90 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Uncle Chipps Plain Salted', 'Uncle Chipps', 'Potato Chips', '50 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Doritos Nacho Cheese', 'Doritos', 'Corn Chips', '100 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Pringles Original', 'Pringles', 'Potato Crisps', '107 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Kellogg''s Corn Flakes', 'Kellogg''s', 'Breakfast Cereal', '300 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Kellogg''s Chocos', 'Kellogg''s', 'Breakfast Cereal', '250 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Nestlé Koko Krunch', 'Nestlé', 'Breakfast Cereal', '170 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Yippee! Magic Masala Noodles', 'Sunfeast', 'Instant Noodles', '70 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Top Ramen Curry Noodles', 'Nissin', 'Instant Noodles', '70 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Knorr Instant Noodles', 'Knorr', 'Instant Noodles', '70 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Amul Taaza Toned Milk', 'Amul', 'Milk', '1 L', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Amul Butter', 'Amul', 'Dairy', '100 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Amul Cheese Slices', 'Amul', 'Dairy', '200 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Kissan Tomato Ketchup', 'Kissan', 'Sauce', '500 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Veeba Eggless Mayonnaise', 'Veeba', 'Sauce', '250 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Maggi Tomato Ketchup', 'Nestlé', 'Sauce', '500 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Cadbury Dairy Milk', 'Cadbury', 'Chocolate', '110 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Cadbury 5 Star', 'Cadbury', 'Chocolate', '40 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('KitKat 4 Finger', 'KitKat', 'Chocolate', '41.5 g', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Pepsi', 'Pepsi', 'Carbonated Beverage', '750 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Thums Up', 'Thums Up', 'Carbonated Beverage', '750 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Fanta Orange', 'Fanta', 'Carbonated Beverage', '750 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Maaza Mango', 'Maaza', 'Fruit Beverage', '600 ml', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Real Fruit Power Mixed Fruit', 'Real', 'Fruit Beverage', '1 L', 'DEMO_VERIFY');
INSERT INTO products
(product_name, brand, category, standard_pack_size, source_status)
VALUES ('Paper Boat Aamras', 'Paper Boat', 'Fruit Beverage', '600 ml', 'DEMO_VERIFY');

-- Example compliance-rule catalogue for your rule engine.
-- These are rule categories, not a legal certification of any particular product.
DROP TABLE IF EXISTS compliance_rules;

CREATE TABLE compliance_rules (
    rule_id INT AUTO_INCREMENT PRIMARY KEY,
    rule_code VARCHAR(50) UNIQUE NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    rule_description TEXT NOT NULL,
    severity ENUM('INFO','WARNING','ERROR') NOT NULL
);

INSERT INTO compliance_rules
(rule_code, field_name, rule_description, severity) VALUES
('LBL001','product_name','Check that the name/description of the food is declared.','ERROR'),
('LBL002','ingredients','Check ingredients declaration where applicable.','ERROR'),
('LBL003','net_quantity','Check net quantity declaration.','ERROR'),
('LBL004','mrp','Check retail sale price against the package/batch record.','ERROR'),
('LBL005','fssai_license_no','Check FSSAI licence number/logo information where applicable.','ERROR'),
('LBL006','veg_nonveg','Check applicable vegetarian/non-vegetarian declaration.','ERROR'),
('LBL007','customer_care_details','Check consumer-care/contact declaration where applicable.','WARNING'),
('LBL008','country_of_origin','Check country-of-origin information where applicable.','WARNING'),
('LBL009','batch_no','Check lot/batch/code information where applicable.','WARNING'),
('LBL010','manufacturing_date','Check date of manufacture/packing where applicable.','WARNING'),
('LBL011','expiry_date','Check expiry/use-by/best-before information as applicable.','ERROR'),
('LBL012','allergens','Check applicable allergen declaration against ingredients.','WARNING');

-- Useful view for the frontend/API
DROP VIEW IF EXISTS product_compliance_input;

CREATE VIEW product_compliance_input AS
SELECT
    p.product_id,
    p.product_name,
    p.brand,
    p.category,
    p.standard_pack_size,
    p.barcode,
    p.manufacturer,
    p.ingredients,
    p.allergens,
    p.veg_nonveg,
    p.fssai_license_no,
    p.country_of_origin,
    p.customer_care_details,
    p.package_type,
    b.batch_no,
    b.mrp,
    b.manufacturing_date,
    b.expiry_date,
    b.net_quantity
FROM products p
LEFT JOIN product_batches b ON p.product_id = b.product_id;
