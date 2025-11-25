# PHP Examples - TECHli Email Security API

PHP integration examples for WordPress, Laravel, and standalone scripts.

## 📦 Requirements

- PHP 7.4 or higher
- `curl` or `allow_url_fopen` enabled

## 🚀 Quick Start

### Check a Single Domain

```bash
php check-domain.php example.com
```

### Get JSON Output

```bash
php check-domain.php example.com --json
```

## 💡 Integration Examples

### WordPress Plugin

```php
<?php
/**
 * Plugin Name: Email Security Checker
 * Description: Check email security for domains
 */

add_action('admin_menu', 'email_security_menu');

function email_security_menu() {
    add_menu_page(
        'Email Security',
        'Email Security',
        'manage_options',
        'email-security',
        'email_security_page'
    );
}

function email_security_page() {
    if (isset($_POST['domain'])) {
        $domain = sanitize_text_field($_POST['domain']);
        $result = check_email_security($domain);
        
        echo '<div class="notice notice-info">';
        echo '<p>Score: ' . $result['overallScore'] . '/100</p>';
        echo '</div>';
    }
    
    ?>
    <div class="wrap">
        <h1>Email Security Checker</h1>
        <form method="post">
            <input type="text" name="domain" placeholder="example.com" required>
            <button type="submit" class="button button-primary">Check</button>
        </form>
    </div>
    <?php
}

function check_email_security($domain) {
    $response = wp_remote_post('https://techli.nz/api/test-domain', [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode(['domain' => $domain])
    ]);
    
    return json_decode(wp_remote_retrieve_body($response), true);
}
```

### Laravel Controller

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class EmailSecurityController extends Controller
{
    public function check(Request $request)
    {
        $request->validate([
            'domain' => 'required|string'
        ]);
        
        $response = Http::post('https://techli.nz/api/test-domain', [
            'domain' => $request->domain
        ]);
        
        $result = $response->json();
        
        return view('email-security.result', [
            'domain' => $request->domain,
            'score' => $result['overallScore'],
            'result' => $result
        ]);
    }
    
    public function checkOnboarding(Request $request)
    {
        $domain = $request->company_domain;
        
        $response = Http::post('https://techli.nz/api/test-domain', [
            'domain' => $domain
        ]);
        
        $result = $response->json();
        
        if ($result['overallScore'] < 70) {
            return back()->with('warning', 
                'Your email security needs attention (Score: ' . 
                $result['overallScore'] . '/100)'
            );
        }
        
        // Continue with onboarding
        return redirect()->route('onboarding.next');
    }
}
```

### Scheduled Check (Laravel)

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use App\Models\Domain;

class CheckEmailSecurity extends Command
{
    protected $signature = 'email:check-security';
    protected $description = 'Check email security for all monitored domains';

    public function handle()
    {
        $domains = Domain::where('monitor_security', true)->get();
        
        foreach ($domains as $domain) {
            $this->info("Checking {$domain->name}...");
            
            $response = Http::post('https://techli.nz/api/test-domain', [
                'domain' => $domain->name
            ]);
            
            $result = $response->json();
            
            // Update database
            $domain->update([
                'last_security_check' => now(),
                'security_score' => $result['overallScore']
            ]);
            
            // Alert if score drops
            if ($result['overallScore'] < 70) {
                $this->warn("⚠️  {$domain->name} score: {$result['overallScore']}/100");
                // Send notification
            }
        }
        
        $this->info('Security check complete!');
    }
}
```

## 🆘 Support

- Email: support@techli.nz
- API Docs: https://techli.nz/api-docs
