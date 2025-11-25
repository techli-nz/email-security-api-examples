# Python Examples - TECHli Email Security API

Python scripts for integrating the TECHli Email Security API.

## 📦 Requirements

```bash
pip install requests
```

No other dependencies needed!

## 🚀 Quick Start

### Check a Single Domain

```bash
python check_domain.py example.com
```

**Output:**
```
============================================================
  EMAIL SECURITY REPORT: example.com
============================================================

Overall Score: 85/100
Compliance: COMPLIANT

SPF:      ✅ PASS
          SPF record found and valid
          Record: v=spf1 include:_spf.example.com ~all

DKIM:     ✅ PASS
          DKIM record found
          Selector: default

DMARC:    ✅ PASS
          DMARC is properly configured
          Policy: quarantine
```

### Get JSON Output

```bash
python check_domain.py example.com --json > result.json
```

### Bulk Check Multiple Domains

Create a `domains.txt` file:
```
example.com
client1.com
client2.com
```

Run bulk check:
```bash
python bulk_check.py domains.txt
```

This generates `email_security_report.csv` with all results.

## 📁 Files

- **`check_domain.py`** - Check single domain with formatted output
- **`bulk_check.py`** - Check multiple domains and generate CSV report
- **`requirements.txt`** - Python dependencies

## 💡 Integration Examples

### Django View

```python
from django.http import JsonResponse
import requests

def check_customer_domain(request, domain):
    """API endpoint to check customer domain."""
    response = requests.post(
        'https://techli.nz/api/test-domain',
        json={'domain': domain}
    )
    result = response.json()
    
    # Store in database or return to frontend
    return JsonResponse(result)
```

### Flask App

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/check-email', methods=['POST'])
def check_email():
    domain = request.json.get('domain')
    
    response = requests.post(
        'https://techli.nz/api/test-domain',
        json={'domain': domain}
    )
    
    return jsonify(response.json())
```

### Scheduled Monitoring

Use with cron to monitor domains daily:

```bash
# Add to crontab (run daily at 9 AM)
0 9 * * * /usr/bin/python3 /path/to/bulk_check.py /path/to/domains.txt
```

## 📊 CSV Report Format

The `bulk_check.py` script generates CSV with:

| Column | Description |
|--------|-------------|
| Domain | Domain name checked |
| Overall Score | Score 0-100 |
| Compliance | compliant/partial/non-compliant |
| SPF | pass/fail/warning |
| DKIM | pass/fail/warning |
| DMARC | pass/fail/warning |
| MX Records | Number of MX records |
| BIMI | pass/fail/warning/N/A |
| MTA-STS | pass/fail/warning/N/A |
| Tested At | ISO timestamp |

## 🆘 Support

- Email: support@techli.nz
- API Docs: https://techli.nz/api-docs
