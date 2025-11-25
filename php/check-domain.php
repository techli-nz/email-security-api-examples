<?php
/**
 * TECHli Email Security API - PHP Example
 * Check a single domain's email security configuration.
 * 
 * Usage:
 *   php check-domain.php example.com
 *   php check-domain.php example.com --json
 */

const API_URL = 'https://techli.nz/api/test-domain';

/**
 * Check email security for a domain
 */
function checkEmailSecurity($domain) {
    $data = json_encode(['domain' => $domain]);
    
    $options = [
        'http' => [
            'method' => 'POST',
            'header' => "Content-Type: application/json\r\n" .
                       "Content-Length: " . strlen($data) . "\r\n",
            'content' => $data,
            'timeout' => 10
        ]
    ];
    
    $context = stream_context_create($options);
    $response = file_get_contents(API_URL, false, $context);
    
    if ($response === false) {
        throw new Exception('Failed to connect to API');
    }
    
    return json_decode($response, true);
}

/**
 * Format status with emoji
 */
function formatStatus($status) {
    $statusMap = [
        'pass' => '✅ PASS',
        'fail' => '❌ FAIL',
        'warning' => '⚠️  WARNING'
    ];
    return $statusMap[$status] ?? strtoupper($status);
}

/**
 * Print formatted report
 */
function printReport($result) {
    echo "\n" . str_repeat('=', 60) . "\n";
    echo "  EMAIL SECURITY REPORT: {$result['domain']}\n";
    echo str_repeat('=', 60) . "\n\n";
    
    echo "Overall Score: {$result['overallScore']}/100\n";
    echo "Compliance: " . strtoupper($result['complianceLevel']) . "\n\n";
    
    // SPF
    echo "SPF:      " . formatStatus($result['spf']['status']) . "\n";
    echo "          {$result['spf']['message']}\n";
    if (isset($result['spf']['record'])) {
        echo "          Record: {$result['spf']['record']}\n";
    }
    echo "\n";
    
    // DKIM
    echo "DKIM:     " . formatStatus($result['dkim']['status']) . "\n";
    echo "          {$result['dkim']['message']}\n";
    if (isset($result['dkim']['selector'])) {
        echo "          Selector: {$result['dkim']['selector']}\n";
    }
    echo "\n";
    
    // DMARC
    echo "DMARC:    " . formatStatus($result['dmarc']['status']) . "\n";
    echo "          {$result['dmarc']['message']}\n";
    if (isset($result['dmarc']['policy'])) {
        echo "          Policy: {$result['dmarc']['policy']}\n";
    }
    echo "\n";
    
    // MX
    echo "MX:       " . formatStatus($result['mx']['status']) . "\n";
    echo "          {$result['mx']['message']}\n";
    foreach ($result['mx']['records'] as $mx) {
        echo "          [{$mx['priority']}] {$mx['exchange']}\n";
    }
    echo "\n";
    
    // BIMI
    if (isset($result['bimi'])) {
        echo "BIMI:     " . formatStatus($result['bimi']['status']) . "\n";
        echo "          {$result['bimi']['message']}\n";
        if (isset($result['bimi']['logoUrl'])) {
            echo "          Logo: {$result['bimi']['logoUrl']}\n";
        }
        echo "\n";
    }
    
    // MTA-STS
    if (isset($result['mtasts'])) {
        echo "MTA-STS:  " . formatStatus($result['mtasts']['status']) . "\n";
        echo "          {$result['mtasts']['message']}\n";
        if (isset($result['mtasts']['mode'])) {
            echo "          Mode: {$result['mtasts']['mode']}\n";
        }
        echo "\n";
    }
    
    echo str_repeat('=', 60) . "\n";
    echo "Tested at: {$result['timestamp']}\n";
    echo str_repeat('=', 60) . "\n\n";
}

// Main execution
if ($argc < 2) {
    echo "Usage: php check-domain.php <domain> [--json]\n";
    echo "Example: php check-domain.php example.com\n";
    exit(1);
}

$domain = $argv[1];
$outputJson = in_array('--json', $argv);

try {
    echo "Checking email security for: $domain...\n";
    $result = checkEmailSecurity($domain);
    
    if ($outputJson) {
        echo json_encode($result, JSON_PRETTY_PRINT) . "\n";
    } else {
        printReport($result);
    }
} catch (Exception $e) {
    echo "❌ Error: " . $e->getMessage() . "\n";
    exit(1);
}
