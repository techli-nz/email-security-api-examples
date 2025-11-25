#!/usr/bin/env python3
"""
TECHli Email Security API - Python Example
Check a single domain's email security configuration.

Usage:
    python check_domain.py example.com
    python check_domain.py example.com --json
"""

import sys
import json
import requests
from typing import Dict, Any


API_URL = "https://techli.nz/api/test-domain"


def check_email_security(domain: str) -> Dict[str, Any]:
    """
    Check email security for a domain using TECHli API.
    
    Args:
        domain: Domain name to check (e.g., 'example.com')
        
    Returns:
        Dictionary containing test results
        
    Raises:
        requests.RequestException: If API request fails
    """
    response = requests.post(
        API_URL,
        json={"domain": domain},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def format_status(status: str) -> str:
    """Format status with color emoji."""
    status_map = {
        "pass": "✅ PASS",
        "fail": "❌ FAIL",
        "warning": "⚠️  WARNING"
    }
    return status_map.get(status, status.upper())


def print_report(result: Dict[str, Any]) -> None:
    """Print a formatted security report."""
    print(f"\n{'='*60}")
    print(f"  EMAIL SECURITY REPORT: {result['domain']}")
    print(f"{'='*60}\n")
    
    # Overall score
    score = result['overallScore']
    compliance = result['complianceLevel'].upper()
    print(f"Overall Score: {score}/100")
    print(f"Compliance: {compliance}\n")
    
    # SPF
    print(f"SPF:      {format_status(result['spf']['status'])}")
    print(f"          {result['spf']['message']}")
    if result['spf'].get('record'):
        print(f"          Record: {result['spf']['record']}")
    print()
    
    # DKIM
    print(f"DKIM:     {format_status(result['dkim']['status'])}")
    print(f"          {result['dkim']['message']}")
    if result['dkim'].get('selector'):
        print(f"          Selector: {result['dkim']['selector']}")
    print()
    
    # DMARC
    print(f"DMARC:    {format_status(result['dmarc']['status'])}")
    print(f"          {result['dmarc']['message']}")
    if result['dmarc'].get('policy'):
        print(f"          Policy: {result['dmarc']['policy']}")
    print()
    
    # MX
    print(f"MX:       {format_status(result['mx']['status'])}")
    print(f"          {result['mx']['message']}")
    for mx in result['mx'].get('records', []):
        print(f"          [{mx['priority']}] {mx['exchange']}")
    print()
    
    # BIMI
    if result.get('bimi'):
        print(f"BIMI:     {format_status(result['bimi']['status'])}")
        print(f"          {result['bimi']['message']}")
        if result['bimi'].get('logoUrl'):
            print(f"          Logo: {result['bimi']['logoUrl']}")
        print()
    
    # MTA-STS
    if result.get('mtasts'):
        print(f"MTA-STS:  {format_status(result['mtasts']['status'])}")
        print(f"          {result['mtasts']['message']}")
        if result['mtasts'].get('mode'):
            print(f"          Mode: {result['mtasts']['mode']}")
        print()
    
    print(f"{'='*60}")
    print(f"Tested at: {result['timestamp']}")
    print(f"{'='*60}\n")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python check_domain.py <domain> [--json]")
        print("Example: python check_domain.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    output_json = "--json" in sys.argv
    
    try:
        print(f"Checking email security for: {domain}...")
        result = check_email_security(domain)
        
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print_report(result)
            
    except requests.RequestException as e:
        print(f"❌ Error: Failed to check domain: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"❌ Error: Unexpected API response format: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
