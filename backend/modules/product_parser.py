"""Extract structured product info from OCR text using regex patterns."""

import re


def parse_product_info(ocr_text):
    """Convert raw OCR text into structured product information.

    Uses regex patterns to find common label fields.
    Returns a dict with all product fields (empty string if not found).
    """
    text = ocr_text if ocr_text else ""
    text_lower = text.lower()

    info = {
        'product_name': extract_product_name(text),
        'manufacturer': extract_field(text, [
            r'(?:mfg\.?|manufactured|mfd\.?)\s*(?:by|:)\s*(.+)',
            r'(?:packed|marketed)\s*(?:by|:)\s*(.+)',
            r'(?:company|brand)\s*:?\s*(.+)',
        ]),
        'packer': extract_field(text, [
            r'(?:packed|pkd\.?)\s*(?:by|:)\s*(.+)',
            r'packer\s*:?\s*(.+)',
        ]),
        'importer': extract_field(text, [
            r'(?:imported|imp\.?)\s*(?:by|:)\s*(.+)',
            r'importer\s*:?\s*(.+)',
        ]),
        'address': extract_address(text),
        'net_quantity': extract_field(text, [
            r'(?:net\s*(?:wt\.?|weight|qty\.?|quantity|content))\s*:?\s*([\d.,]+\s*(?:g|gm|gms|gram|grams|kg|kgs|ml|l|ltr|litre|litres|oz|pieces?|pcs?|units?))',
            r'(\d+\s*(?:g|gm|kg|ml|l|ltr)\b)',
        ]),
        'mrp': extract_field(text, [
            r'(?:mrp|m\.r\.p\.?|max(?:imum)?\s*retail\s*price)\s*:?\s*(?:rs\.?|₹|inr)?\s*([\d.,]+)',
            r'(?:rs\.?|₹)\s*([\d.,]+)',
            r'price\s*:?\s*(?:rs\.?|₹)?\s*([\d.,]+)',
        ]),
        'manufacturing_date': extract_field(text, [
            r'(?:mfg\.?\s*(?:date|dt\.?)|mfd\.?\s*(?:date|dt\.?)|date\s*of\s*(?:mfg|manufacture|manufacturing)|manufactured\s*(?:on|date))\s*:?\s*(.+?)(?:\n|$)',
            r'(?:pkg\.?\s*(?:date|dt\.?))\s*:?\s*(.+?)(?:\n|$)',
        ]),
        'expiry_date': extract_field(text, [
            r'(?:exp(?:iry)?\.?\s*(?:date|dt\.?)?|best\s*before|use\s*before|use\s*by|bb)\s*:?\s*(.+?)(?:\n|$)',
            r'(?:valid\s*(?:till|until|upto))\s*:?\s*(.+?)(?:\n|$)',
        ]),
        'best_before': extract_field(text, [
            r'(?:best\s*before)\s*:?\s*(.+?)(?:\n|$)',
            r'(?:bb)\s*:?\s*(.+?)(?:\n|$)',
        ]),
        'customer_care': extract_field(text, [
            r'(?:customer\s*care|consumer\s*(?:care|helpline|complaint)|toll\s*free|helpline|contact)\s*(?:no\.?|number|:)?\s*:?\s*([\d\s\-+()]+)',
            r'(?:call\s*(?:us)?)\s*:?\s*([\d\s\-+()]+)',
            r'(\d{4}[\s\-]?\d{3}[\s\-]?\d{4})',
            r'(1800[\s\-]?\d{3}[\s\-]?\d{3,4})',
        ]),
        'country_of_origin': extract_field(text, [
            r'(?:country\s*of\s*origin|origin|made\s*in|product\s*of)\s*:?\s*(.+?)(?:\n|$)',
        ]),
        'ingredients': extract_field(text, [
            r'(?:ingredients?|composition)\s*:?\s*(.+?)(?:\n\n|\Z)',
        ]),
        'claims': extract_claims(text),
        'barcode': extract_field(text, [
            r'(\d{8,14})',
        ]),
    }

    # Clean up all values
    for key in info:
        if info[key]:
            info[key] = info[key].strip().strip(':').strip()

    return info


def extract_product_name(text):
    """Extract product name — usually the first prominent line."""
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        # Skip very short lines or lines that look like codes
        if len(line) > 3 and not re.match(r'^[\d\W]+$', line):
            # Skip lines that are clearly field labels
            skip_words = ['mfg', 'exp', 'mrp', 'net', 'best', 'batch', 'customer', 'ingredients', 'packed']
            if not any(line.lower().startswith(w) for w in skip_words):
                return line
    return ""


def extract_field(text, patterns):
    """Try multiple regex patterns, return first match."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    return ""


def extract_address(text):
    """Extract address — look for lines with pin codes or common address patterns."""
    # Look for pin code pattern (6 digits) in context
    match = re.search(
        r'(.{10,100}?\b\d{6}\b)',
        text, re.IGNORECASE
    )
    if match:
        return match.group(1).strip()

    # Look for address-like patterns
    match = re.search(
        r'(?:address|addr\.?|regd\.?\s*off(?:ice)?)\s*:?\s*(.+?)(?:\n\n|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if match:
        return match.group(1).strip()

    return ""


def extract_claims(text):
    """Extract product claims like 'organic', 'sugar-free', etc."""
    claim_words = [
        'organic', 'natural', 'sugar.?free', 'fat.?free', 'preservative.?free',
        'no.?added.?sugar', 'gluten.?free', 'vegan', 'vegetarian', 'non.?gmo',
        'fortified', 'enriched', 'lite', 'light', 'diet', 'zero.?calorie',
        'whole.?grain', 'no.?artificial', 'no.?preservative', 'iso.?certified',
    ]
    found = []
    for claim in claim_words:
        if re.search(claim, text, re.IGNORECASE):
            # Get the actual matched text
            match = re.search(claim, text, re.IGNORECASE)
            found.append(match.group(0))

    return ', '.join(found) if found else ""
