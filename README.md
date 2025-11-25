# TECHli Email Security API - Code Examples

[![API Documentation](https://img.shields.io/badge/API-Documentation-blue)](https://techli.nz/api-docs)
[![OpenAPI Spec](https://img.shields.io/badge/OpenAPI-3.0-green)](https://techli.nz/openapi.yaml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official code examples for integrating the [TECHli Email Security API](https://techli.nz/api-docs) into your applications.

## 🚀 What is TECHli Email Security API?

A **free REST API** for comprehensive email security testing:

- ✅ **SPF** (Sender Policy Framework) validation
- ✅ **DKIM** (DomainKeys Identified Mail) auto-discovery
- ✅ **DMARC** (Domain-based Message Authentication) policy checking
- ✅ **MX** record lookup
- ✅ **WHOIS** domain information
- ✅ **BIMI** (Brand Indicators for Message Identification)
- ✅ **MTA-STS** (Mail Transfer Agent Strict Transport Security)
- ✅ **Overall compliance score** (0-100)

**No API key required** | **100 requests/hour free tier** | **Built in New Zealand**

---

## 📖 Quick Start

```bash
curl -X POST https://techli.nz/api/test-domain \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

**Response:**
```json
{
  "domain": "example.com",
  "overallScore": 85,
  "complianceLevel": "compliant",
  "spf": { "status": "pass", "message": "SPF record found and valid" },
  "dkim": { "status": "pass", "selector": "default" },
  "dmarc": { "status": "pass", "policy": "quarantine" }
}
```

---

## 💻 Code Examples

Choose your language:

### [Python →](python/)
Simple script for testing single domains or bulk processing.

### [Node.js →](nodejs/)
Integration examples for Express/Next.js applications.

### [PHP →](php/)
WordPress plugin and Laravel integration examples.

### [Bash →](bash/)
Shell scripts for automation and cron jobs.

---

## 📚 Common Use Cases

### 1. **SaaS Onboarding**
Validate customer domains during signup to prevent email deliverability issues.

```javascript
// Check domain before allowing customer to proceed
const result = await checkEmailSecurity(customerDomain);
if (result.complianceLevel === 'non-compliant') {
  showWarning('Your email security needs attention');
}
```

### 2. **Monitoring Dashboard**
Track email security across multiple client domains.

```python
# Daily cron job to check all clients
for domain in client_domains:
    result = check_domain(domain)
    if result['overallScore'] < 70:
        send_alert(domain, result)
```

### 3. **Compliance Reporting**
Generate cyber insurance compliance reports automatically.

```php
$report = generateComplianceReport('client-domain.com');
// Returns detailed PDF with all email security checks
```

### 4. **CI/CD Pipeline**
Validate email configuration before deployment.

```bash
# In your .gitlab-ci.yml or GitHub Actions
./check-email-security.sh $DOMAIN_NAME
```

---

## 🎯 Features

- **No authentication required** (free tier)
- **CORS enabled** (works from browser JavaScript)
- **Rate limiting:** 100 requests/hour per IP
- **Response time:** Usually < 2 seconds
- **Uptime:** 99.9% (monitored)

---

## 📊 Response Schema

```typescript
interface DnsTestResult {
  domain: string;
  overallScore: number;              // 0-100
  complianceLevel: 'compliant' | 'partial' | 'non-compliant';
  
  spf: {
    exists: boolean;
    record?: string;
    valid: boolean;
    status: 'pass' | 'fail' | 'warning';
    message: string;
  };
  
  dkim: {
    status: 'pass' | 'fail' | 'warning';
    message: string;
    selector?: string;
    record?: string;
  };
  
  dmarc: {
    exists: boolean;
    record?: string;
    policy?: 'none' | 'quarantine' | 'reject';
    valid: boolean;
    status: 'pass' | 'fail' | 'warning';
    message: string;
  };
  
  mx: {
    records: Array<{ exchange: string; priority: number }>;
    status: 'pass' | 'fail' | 'warning';
    message: string;
  };
  
  whois: {
    registrarName?: string;
    status: 'pass' | 'fail' | 'warning';
    message: string;
  };
  
  bimi: {
    exists: boolean;
    logoUrl?: string;
    status: 'pass' | 'fail' | 'warning';
    message: string;
  };
  
  mtasts: {
    exists: boolean;
    mode?: 'enforce' | 'testing' | 'none';
    status: 'pass' | 'fail' | 'warning';
    message: string;
  };
  
  timestamp: string;
}
```

---

## 🆘 Support

- **API Documentation:** https://techli.nz/api-docs
- **Email:** support@techli.nz
- **Issues:** [GitHub Issues](https://github.com/techli-nz/email-security-api-examples/issues)
- **Website:** https://techli.nz

---

## 🤝 Contributing

Found a bug or want to add an example in another language?

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/java-example`)
3. Commit your changes (`git commit -am 'Add Java integration example'`)
4. Push to the branch (`git push origin feature/java-example`)
5. Open a Pull Request

---

## 📝 License

MIT License - Free for commercial and non-commercial use.

See [LICENSE](LICENSE) file for details.

---

## 🌟 About TECHli

We're a New Zealand IT support company specializing in email security, managed services, and cyber insurance compliance for SMBs.

**We don't just test email security - we fix it too.**

- 🌐 **Website:** https://techli.nz
- 💼 **Services:** Managed IT, Email Security, Compliance
- 📍 **Location:** Auckland, New Zealand

---

## ⭐ Star This Repo

If you find this API useful, please star this repository to help others discover it!

[![GitHub stars](https://img.shields.io/github/stars/techli-nz/email-security-api-examples?style=social)](https://github.com/techli-nz/email-security-api-examples)
