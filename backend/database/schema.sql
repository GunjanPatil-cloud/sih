-- ============================================
-- SIH Packaged Commodity Compliance System
-- Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS sih_compliance
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE sih_compliance;

-- ============================================
-- Users
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================
-- Products (local sample product database)
-- ============================================
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(50) UNIQUE,
    product_name VARCHAR(255),
    category VARCHAR(100),
    manufacturer VARCHAR(255),
    packer VARCHAR(255),
    importer VARCHAR(255),
    address TEXT,
    net_quantity VARCHAR(100),
    mrp VARCHAR(50),
    manufacturing_date VARCHAR(50),
    expiry_date VARCHAR(50),
    best_before VARCHAR(100),
    customer_care VARCHAR(255),
    country_of_origin VARCHAR(100),
    ingredients TEXT,
    claims TEXT,
    is_demo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================
-- Product Scans
-- ============================================
CREATE TABLE IF NOT EXISTS product_scans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(255),
    barcode VARCHAR(50),
    scan_method ENUM('image', 'barcode', 'qr', 'manual') DEFAULT 'manual',
    image_path VARCHAR(500),
    ocr_text TEXT,
    extracted_info JSON,
    compliance_score DECIMAL(5,2),
    compliance_status ENUM('compliant', 'partially_compliant', 'non_compliant') DEFAULT 'non_compliant',
    passed_count INT DEFAULT 0,
    warning_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================
-- Compliance Rules
-- ============================================
CREATE TABLE IF NOT EXISTS compliance_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(50) NOT NULL UNIQUE,
    rule_name VARCHAR(255) NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    description TEXT,
    is_required TINYINT(1) DEFAULT 1,
    severity ENUM('HIGH', 'MEDIUM', 'LOW') DEFAULT 'MEDIUM',
    failure_message TEXT,
    recommendation TEXT,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================
-- Compliance Results (per-rule results for each scan)
-- ============================================
CREATE TABLE IF NOT EXISTS compliance_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scan_id INT NOT NULL,
    rule_id VARCHAR(50) NOT NULL,
    status ENUM('PASS', 'WARNING', 'FAIL', 'NOT_APPLICABLE') DEFAULT 'FAIL',
    field_value TEXT,
    message TEXT,
    FOREIGN KEY (scan_id) REFERENCES product_scans(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- Indexes for performance
-- ============================================
CREATE INDEX idx_products_barcode ON products(barcode);
CREATE INDEX idx_scans_product ON product_scans(product_id);
CREATE INDEX idx_scans_date ON product_scans(scanned_at);
CREATE INDEX idx_results_scan ON compliance_results(scan_id);
CREATE INDEX idx_rules_active ON compliance_rules(is_active);
