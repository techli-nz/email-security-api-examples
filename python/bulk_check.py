#!/usr/bin/env python3
"""
TECHli Email Security API - Bulk Domain Checker
Check multiple domains and generate a CSV report.

Usage:
    python bulk_check.py domains.txt
    python bulk_check.py domains.txt --output report.csv
"""

import sys
import csv
import time
import requests
from typing import List, Dict, Any
from pathlib import Path


API_URL = "https://techli.nz/api/test-domain"
RATE_LIMIT_DELAY = 1.5  # Seconds between requests (stay under 100/hour)


def check_domain(domain: str) -> Dict[str, Any]:
    """Check a single domain."""
    try:
        response = requests.post(
            API_URL,
            json={"domain": domain},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "domain": domain,
            "error": str(e),
            "overallScore": 0,
            "complianceLevel": "error"
        }


def load_domains(filename: str) -> List[str]:
    """Load domains from file (one per line)."""
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    domains = []
    with open(path, 'r') as f:
        for line in f:
            domain = line.strip()
            if domain and not domain.startswith('#'):
                domains.append(domain)
    
    return domains


def save_csv_report(results: List[Dict[str, Any]], output_file: str):
    """Save results to CSV file."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Domain',
            'Overall Score',
            'Compliance',
            'SPF',
            'DKIM',
            'DMARC',
            'MX Records',
            'BIMI',
            'MTA-STS',
            'Tested At'
        ])
        
        # Data rows
        for result in results:
            if 'error' in result:
                writer.writerow([
                    result['domain'],
                    '0',
                    'ERROR',
                    result['error'],
                    '', '', '', '', '', ''
                ])
            else:
                writer.writerow([
                    result['domain'],
                    result['overallScore'],
                    result['complianceLevel'],
                    result['spf']['status'],
                    result['dkim']['status'],
                    result['dmarc']['status'],
                    len(result['mx']['records']),
                    result.get('bimi', {}).get('status', 'N/A'),
                    result.get('mtasts', {}).get('status', 'N/A'),
                    result['timestamp']
                ])


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python bulk_check.py <domains.txt> [--output report.csv]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "email_security_report.csv"
    
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    try:
        # Load domains
        print(f"Loading domains from: {input_file}")
        domains = load_domains(input_file)
        print(f"Found {len(domains)} domain(s) to check\n")
        
        # Check each domain
        results = []
        for i, domain in enumerate(domains, 1):
            print(f"[{i}/{len(domains)}] Checking {domain}...", end=' ')
            
            result = check_domain(domain)
            results.append(result)
            
            if 'error' in result:
                print(f"❌ ERROR: {result['error']}")
            else:
                score = result['overallScore']
                print(f"✅ Score: {score}/100")
            
            # Rate limiting
            if i < len(domains):
                time.sleep(RATE_LIMIT_DELAY)
        
        # Save report
        print(f"\nSaving report to: {output_file}")
        save_csv_report(results, output_file)
        
        # Summary
        avg_score = sum(r['overallScore'] for r in results) / len(results)
        compliant = sum(1 for r in results if r.get('complianceLevel') == 'compliant')
        
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Total domains checked: {len(domains)}")
        print(f"Average score: {avg_score:.1f}/100")
        print(f"Fully compliant: {compliant}/{len(domains)}")
        print(f"{'='*60}\n")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
