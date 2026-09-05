"""Compliance engine — rule-based verification against configurable rules."""

import json
import os
from config import Config


def load_rules(rules_path=None):
    """Load compliance rules from JSON file."""
    path = rules_path or Config.RULES_PATH
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[COMPLIANCE] Could not load rules: {e}")
        return []


def check_compliance(product_info, rules=None):
    """Run all active compliance rules against product information.

    Args:
        product_info: dict with product fields (from product_parser)
        rules: list of rule dicts (loaded from JSON if not provided)

    Returns: dict with score, status, results list, and counts.
    """
    if rules is None:
        rules = load_rules()

    results = []
    passed = 0
    warnings = 0
    failed = 0
    na_count = 0

    for rule in rules:
        field = rule.get('field', '')
        value = product_info.get(field, '').strip()
        is_required = rule.get('is_required', True)
        severity = rule.get('severity', 'MEDIUM')

        # Determine status
        if value:
            status = 'PASS'
            message = f"'{rule.get('rule_name', field)}' is declared."
            passed += 1
        elif is_required:
            status = 'FAIL'
            message = rule.get('failure_message', f"Required field '{field}' is missing.")
            failed += 1
        else:
            # Optional field missing → WARNING if medium/high severity, NA if low
            if severity == 'LOW':
                status = 'NOT_APPLICABLE'
                message = f"Optional field '{field}' — not applicable or not found."
                na_count += 1
            else:
                status = 'WARNING'
                message = rule.get('failure_message', f"Optional field '{field}' is missing.")
                warnings += 1

        results.append({
            'rule_id': rule.get('rule_id', ''),
            'rule_name': rule.get('rule_name', ''),
            'field': field,
            'status': status,
            'severity': severity,
            'value_found': value if value else None,
            'message': message,
            'recommendation': rule.get('recommendation', ''),
            'description': rule.get('description', ''),
        })

    # Calculate score
    total_applicable = passed + warnings + failed
    if total_applicable > 0:
        # Passed = full weight, warnings = half weight, failed = 0
        score = round(((passed + (warnings * 0.5)) / total_applicable) * 100, 1)
    else:
        score = 0

    # Determine overall status
    if score >= 100:
        overall_status = 'compliant'
        status_label = 'Fully Compliant'
    elif score >= 75:
        overall_status = 'partially_compliant'
        status_label = 'Mostly Compliant'
    elif score >= 50:
        overall_status = 'partially_compliant'
        status_label = 'Needs Attention'
    else:
        overall_status = 'non_compliant'
        status_label = 'Non-Compliant'

    return {
        'score': score,
        'status': overall_status,
        'status_label': status_label,
        'passed': passed,
        'warnings': warnings,
        'failed': failed,
        'not_applicable': na_count,
        'total_rules': len(rules),
        'results': results,
    }


def get_score_color(score):
    """Return a CSS color class based on score."""
    if score >= 90:
        return 'pass'
    elif score >= 60:
        return 'warning'
    else:
        return 'fail'
