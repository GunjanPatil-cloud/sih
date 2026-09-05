"""Scan routes — image upload, OCR extraction, compliance check."""

import os
import uuid
import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from config import Config
from database.db import execute_query
from modules.ocr import extract_text
from modules.product_parser import parse_product_info
from modules.compliance_engine import check_compliance, get_score_color

scan_bp = Blueprint('scan', __name__)

ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def safe_filename(filename):
    """Generate a safe unique filename preserving the extension."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'
    return f"{uuid.uuid4().hex}.{ext}"


@scan_bp.route('/scan')
def scan_page():
    """Scan / upload page."""
    return render_template('scan.html')


@scan_bp.route('/api/products/search')
def search_products():
    """Find products by name, brand, or barcode for the scanner lookup."""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({'success': True, 'products': []})

    pattern = f'%{query}%'
    products = execute_query(
        """
        SELECT product_id, product_name, brand, category, standard_pack_size,
               barcode, manufacturer, source_status
        FROM products
        WHERE product_name LIKE %s OR brand LIKE %s OR barcode LIKE %s
        ORDER BY product_name
        LIMIT 8
        """,
        (pattern, pattern, pattern),
        fetch=True,
    )

    # Support the original project schema until the supplied seed is imported.
    if products is None:
        products = execute_query(
            """
            SELECT id AS product_id, product_name, NULL AS brand,
                   category, net_quantity AS standard_pack_size, barcode,
                   manufacturer, NULL AS source_status
            FROM products
            WHERE product_name LIKE %s OR barcode LIKE %s
            ORDER BY product_name
            LIMIT 8
            """,
            (pattern, pattern),
            fetch=True,
        )

    return jsonify({'success': True, 'products': products or []})


@scan_bp.route('/api/scan/image', methods=['POST'])
def upload_and_process():
    """Handle image upload → OCR → parse → compliance check → return results."""

    # --- Validate upload ---
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    # --- Save file ---
    filename = safe_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    # --- OCR Extraction ---
    ocr_result = extract_text(filepath)
    ocr_text = ocr_result.get('text', '')

    # --- Parse product info from OCR text ---
    product_info = parse_product_info(ocr_text)

    # --- Run compliance check ---
    compliance = check_compliance(product_info)

    return jsonify({
        'success': True,
        'filename': filename,
        'filepath': filepath,
        'original_name': file.filename,
        'ocr': {
            'text': ocr_text,
            'word_count': ocr_result.get('word_count', 0),
            'confidence': ocr_result.get('confidence', 0),
        },
        'product_info': product_info,
        'compliance': compliance,
    })


@scan_bp.route('/api/compliance/check', methods=['POST'])
def check_manual():
    """Check compliance from manually entered product data (JSON body)."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No product data provided'}), 400

    compliance = check_compliance(data)
    return jsonify({
        'success': True,
        'product_info': data,
        'compliance': compliance,
    })


@scan_bp.route('/result')
def result_page():
    """Results page — renders with data passed via query params or session."""
    return render_template('result.html')
