#!/bin/bash
# TECHli Email Security API - Bash Script
# Check a single domain's email security configuration.
#
# Usage:
#   ./check-domain.sh example.com
#   ./check-domain.sh example.com --json

set -e

API_URL="https://techli.nz/api/test-domain"

# Check if domain provided
if [ -z "$1" ]; then
    echo "Usage: $0 <domain> [--json]"
    echo "Example: $0 example.com"
    exit 1
fi

DOMAIN="$1"
OUTPUT_JSON=false

if [ "$2" = "--json" ]; then
    OUTPUT_JSON=true
fi

# Make API request
RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "{\"domain\": \"$DOMAIN\"}")

# Check if jq is available
if command -v jq &> /dev/null; then
    if [ "$OUTPUT_JSON" = true ]; then
        echo "$RESPONSE" | jq '.'
    else
        # Pretty print report
        echo ""
        echo "============================================================"
        echo "  EMAIL SECURITY REPORT: $DOMAIN"
        echo "============================================================"
        echo ""
        
        SCORE=$(echo "$RESPONSE" | jq -r '.overallScore')
        COMPLIANCE=$(echo "$RESPONSE" | jq -r '.complianceLevel' | tr '[:lower:]' '[:upper:]')
        
        echo "Overall Score: $SCORE/100"
        echo "Compliance: $COMPLIANCE"
        echo ""
        
        # SPF
        SPF_STATUS=$(echo "$RESPONSE" | jq -r '.spf.status')
        SPF_MSG=$(echo "$RESPONSE" | jq -r '.spf.message')
        echo "SPF:      [$SPF_STATUS] $SPF_MSG"
        
        # DKIM
        DKIM_STATUS=$(echo "$RESPONSE" | jq -r '.dkim.status')
        DKIM_MSG=$(echo "$RESPONSE" | jq -r '.dkim.message')
        echo "DKIM:     [$DKIM_STATUS] $DKIM_MSG"
        
        # DMARC
        DMARC_STATUS=$(echo "$RESPONSE" | jq -r '.dmarc.status')
        DMARC_MSG=$(echo "$RESPONSE" | jq -r '.dmarc.message')
        DMARC_POLICY=$(echo "$RESPONSE" | jq -r '.dmarc.policy // "none"')
        echo "DMARC:    [$DMARC_STATUS] $DMARC_MSG (policy: $DMARC_POLICY)"
        
        # MX
        MX_STATUS=$(echo "$RESPONSE" | jq -r '.mx.status')
        MX_COUNT=$(echo "$RESPONSE" | jq -r '.mx.records | length')
        echo "MX:       [$MX_STATUS] $MX_COUNT record(s) found"
        
        echo ""
        echo "============================================================"
        
        TIMESTAMP=$(echo "$RESPONSE" | jq -r '.timestamp')
        echo "Tested at: $TIMESTAMP"
        echo "============================================================"
        echo ""
    fi
else
    # jq not available, just print raw JSON
    echo "$RESPONSE"
    echo ""
    echo "Note: Install 'jq' for formatted output"
fi
