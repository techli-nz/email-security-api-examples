# Bash Examples - TECHli Email Security API

Shell scripts for automation and monitoring.

## 📦 Requirements

- `curl` (usually pre-installed)
- `jq` (optional, for formatted output)

Install jq:
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# CentOS/RHEL
sudo yum install jq
```

## 🚀 Quick Start

### Make Script Executable

```bash
chmod +x check-domain.sh
```

### Check a Domain

```bash
./check-domain.sh example.com
```

### Get JSON Output

```bash
./check-domain.sh example.com --json
```

## 💡 Use Cases

### Cron Job Monitoring

Add to crontab to check domains daily:

```bash
# Edit crontab
crontab -e

# Add this line (runs every day at 9 AM)
0 9 * * * /path/to/check-domain.sh client-domain.com >> /var/log/email-security.log 2>&1
```

### CI/CD Pipeline

Use in GitLab CI or GitHub Actions:

```yaml
# .gitlab-ci.yml
test-email-security:
  script:
    - bash check-domain.sh $PRODUCTION_DOMAIN
    - if [ $? -ne 0 ]; then exit 1; fi
```

### Bulk Domain Checking

```bash
#!/bin/bash
# check-all-domains.sh

DOMAINS=(
  "client1.com"
  "client2.com"
  "client3.com"
)

for domain in "${DOMAINS[@]}"; do
  echo "Checking $domain..."
  ./check-domain.sh "$domain"
  sleep 2  # Rate limiting
done
```

### Alert on Low Score

```bash
#!/bin/bash
# alert-if-low-score.sh

DOMAIN="$1"
RESPONSE=$(curl -s -X POST "https://techli.nz/api/test-domain" \
    -H "Content-Type: application/json" \
    -d "{\"domain\": \"$DOMAIN\"}")

SCORE=$(echo "$RESPONSE" | jq -r '.overallScore')

if [ "$SCORE" -lt 70 ]; then
    echo "⚠️  WARNING: $DOMAIN has low score: $SCORE/100"
    # Send email alert
    echo "Email security issues detected for $DOMAIN" | mail -s "Alert: Low Email Security Score" admin@example.com
fi
```

## 🆘 Support

- Email: support@techli.nz
- API Docs: https://techli.nz/api-docs
