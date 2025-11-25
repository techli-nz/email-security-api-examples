/**
 * TECHli Email Security API - Express.js Integration Example
 * 
 * Install dependencies:
 *   npm install express axios
 * 
 * Run:
 *   node express-example.js
 */

const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

app.use(express.json());

/**
 * Check email security endpoint
 */
app.post('/api/check-email', async (req, res) => {
  const { domain } = req.body;
  
  if (!domain) {
    return res.status(400).json({ error: 'Domain is required' });
  }
  
  try {
    const response = await axios.post('https://techli.nz/api/test-domain', {
      domain: domain
    });
    
    // Return results to client
    res.json(response.data);
    
  } catch (error) {
    console.error('Error checking domain:', error.message);
    res.status(500).json({ 
      error: 'Failed to check domain',
      message: error.message 
    });
  }
});

/**
 * Example: Check domain during user onboarding
 */
app.post('/api/onboard-customer', async (req, res) => {
  const { email, companyName, domain } = req.body;
  
  try {
    // Check email security
    const securityCheck = await axios.post('https://techli.nz/api/test-domain', {
      domain: domain
    });
    
    const result = securityCheck.data;
    
    // Warn if email security is poor
    if (result.overallScore < 70) {
      return res.status(200).json({
        success: true,
        warning: 'Email security needs attention',
        issues: {
          spf: result.spf.status !== 'pass',
          dkim: result.dkim.status !== 'pass',
          dmarc: result.dmarc.status !== 'pass'
        },
        recommendation: 'We recommend fixing email security before proceeding'
      });
    }
    
    // Proceed with onboarding
    res.json({
      success: true,
      message: 'Email security looks good!',
      score: result.overallScore
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Example: Get compliance report
 */
app.get('/api/compliance-report/:domain', async (req, res) => {
  const { domain } = req.params;
  
  try {
    const response = await axios.post('https://techli.nz/api/test-domain', {
      domain: domain
    });
    
    const result = response.data;
    
    // Generate compliance report
    const report = {
      domain: domain,
      testedAt: new Date().toISOString(),
      overallScore: result.overallScore,
      complianceLevel: result.complianceLevel,
      checks: {
        spf: {
          passed: result.spf.status === 'pass',
          details: result.spf.message
        },
        dkim: {
          passed: result.dkim.status === 'pass',
          details: result.dkim.message
        },
        dmarc: {
          passed: result.dmarc.status === 'pass',
          details: result.dmarc.message,
          policy: result.dmarc.policy
        }
      },
      cyberInsuranceReady: result.overallScore >= 80
    };
    
    res.json(report);
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log('\nEndpoints:');
  console.log(`  POST /api/check-email - Check domain email security`);
  console.log(`  POST /api/onboard-customer - Customer onboarding with security check`);
  console.log(`  GET /api/compliance-report/:domain - Get compliance report`);
});
