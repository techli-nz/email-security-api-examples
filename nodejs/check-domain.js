#!/usr/bin/env node
/**
 * TECHli Email Security API - Node.js Example
 * Check a single domain's email security configuration.
 * 
 * Usage:
 *   node check-domain.js example.com
 *   node check-domain.js example.com --json
 */

const https = require('https');

const API_URL = 'https://techli.nz/api/test-domain';

/**
 * Check email security for a domain
 */
async function checkEmailSecurity(domain) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ domain });
    
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };
    
    const req = https.request(API_URL, options, (res) => {
      let body = '';
      
      res.on('data', (chunk) => {
        body += chunk;
      });
      
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve(result);
        } catch (e) {
          reject(new Error('Invalid JSON response'));
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * Format status with emoji
 */
function formatStatus(status) {
  const statusMap = {
    'pass': '✅ PASS',
    'fail': '❌ FAIL',
    'warning': '⚠️  WARNING'
  };
  return statusMap[status] || status.toUpperCase();
}

/**
 * Print formatted report
 */
function printReport(result) {
  console.log('\n' + '='.repeat(60));
  console.log(`  EMAIL SECURITY REPORT: ${result.domain}`);
  console.log('='.repeat(60) + '\n');
  
  console.log(`Overall Score: ${result.overallScore}/100`);
  console.log(`Compliance: ${result.complianceLevel.toUpperCase()}\n`);
  
  // SPF
  console.log(`SPF:      ${formatStatus(result.spf.status)}`);
  console.log(`          ${result.spf.message}`);
  if (result.spf.record) {
    console.log(`          Record: ${result.spf.record}`);
  }
  console.log();
  
  // DKIM
  console.log(`DKIM:     ${formatStatus(result.dkim.status)}`);
  console.log(`          ${result.dkim.message}`);
  if (result.dkim.selector) {
    console.log(`          Selector: ${result.dkim.selector}`);
  }
  console.log();
  
  // DMARC
  console.log(`DMARC:    ${formatStatus(result.dmarc.status)}`);
  console.log(`          ${result.dmarc.message}`);
  if (result.dmarc.policy) {
    console.log(`          Policy: ${result.dmarc.policy}`);
  }
  console.log();
  
  // MX
  console.log(`MX:       ${formatStatus(result.mx.status)}`);
  console.log(`          ${result.mx.message}`);
  result.mx.records.forEach(mx => {
    console.log(`          [${mx.priority}] ${mx.exchange}`);
  });
  console.log();
  
  // BIMI
  if (result.bimi) {
    console.log(`BIMI:     ${formatStatus(result.bimi.status)}`);
    console.log(`          ${result.bimi.message}`);
    if (result.bimi.logoUrl) {
      console.log(`          Logo: ${result.bimi.logoUrl}`);
    }
    console.log();
  }
  
  // MTA-STS
  if (result.mtasts) {
    console.log(`MTA-STS:  ${formatStatus(result.mtasts.status)}`);
    console.log(`          ${result.mtasts.message}`);
    if (result.mtasts.mode) {
      console.log(`          Mode: ${result.mtasts.mode}`);
    }
    console.log();
  }
  
  console.log('='.repeat(60));
  console.log(`Tested at: ${result.timestamp}`);
  console.log('='.repeat(60) + '\n');
}

/**
 * Main function
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('Usage: node check-domain.js <domain> [--json]');
    console.error('Example: node check-domain.js example.com');
    process.exit(1);
  }
  
  const domain = args[0];
  const outputJson = args.includes('--json');
  
  try {
    console.log(`Checking email security for: ${domain}...`);
    const result = await checkEmailSecurity(domain);
    
    if (outputJson) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      printReport(result);
    }
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
