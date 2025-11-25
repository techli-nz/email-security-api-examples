# Node.js Examples - TECHli Email Security API

Node.js integration examples for the TECHli Email Security API.

## 📦 Installation

### Using npm:
```bash
npm install axios
```

### No dependencies (using built-in https):
The `check-domain.js` script uses only Node.js built-in modules!

## 🚀 Quick Start

### Check a Single Domain

```bash
node check-domain.js example.com
```

### Get JSON Output

```bash
node check-domain.js example.com --json
```

### Express.js Integration

```bash
npm install express axios
node express-example.js
```

Then test:
```bash
curl -X POST http://localhost:3000/api/check-email \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

## 📁 Files

- **`check-domain.js`** - Standalone script (no dependencies)
- **`express-example.js`** - Express.js API integration
- **`package.json`** - Dependencies for Express example

## 💡 Integration Examples

### Next.js API Route

```javascript
// pages/api/check-email.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  const { domain } = req.body;
  
  try {
    const response = await axios.post('https://techli.nz/api/test-domain', {
      domain: domain
    });
    
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

### React Hook

```javascript
// hooks/useEmailSecurity.js
import { useState } from 'react';

export function useEmailSecurity() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  const checkDomain = async (domain) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('https://techli.nz/api/test-domain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return { checkDomain, loading, result, error };
}
```

### Scheduled Job (node-cron)

```javascript
const cron = require('node-cron');
const axios = require('axios');

// Check domains every day at 9 AM
cron.schedule('0 9 * * *', async () => {
  const domains = ['client1.com', 'client2.com', 'client3.com'];
  
  for (const domain of domains) {
    try {
      const result = await axios.post('https://techli.nz/api/test-domain', {
        domain: domain
      });
      
      if (result.data.overallScore < 70) {
        console.log(`⚠️  ${domain} needs attention (score: ${result.data.overallScore})`);
        // Send alert email
      }
    } catch (error) {
      console.error(`Error checking ${domain}:`, error.message);
    }
  }
});
```

## 🆘 Support

- Email: support@techli.nz
- API Docs: https://techli.nz/api-docs
