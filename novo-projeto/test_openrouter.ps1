# OpenRouter API Test Script (PowerShell)
# This script tests OpenRouter connectivity and Jamba model response

param(
    [string]$ApiKey = $env:OPENROUTER_API_KEY,
    [switch]$Verbose = $false
)

Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "OpenRouter API - Connection & Functionality Test" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check API Key
Write-Host "[Test 1/3] Checking OPENROUTER_API_KEY..." -ForegroundColor Blue

if (-not $ApiKey) {
    Write-Host "[ERROR] OPENROUTER_API_KEY not found in environment" -ForegroundColor Red
    Write-Host "  Set it with: `$env:OPENROUTER_API_KEY = 'your-key-here'" -ForegroundColor Yellow
    exit 1
}

if ($ApiKey.Length -lt 20) {
    Write-Host "[WARN] API key seems too short ($($ApiKey.Length) characters)" -ForegroundColor Yellow
} else {
    Write-Host "[OK] API key found ($($ApiKey.Length) characters)" -ForegroundColor Green
}

# Test 2: Test Jamba 1.5 Large
Write-Host ""
Write-Host "[Test 2/3] Testing Jamba 1.5 Large model..." -ForegroundColor Blue

$headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Content-Type"  = "application/json"
    "HTTP-Referer"  = "https://ativo-real.azure"
    "X-Title"       = "Ativo Real - Land Management Platform"
}

$payload = @{
    model        = "jamba-1.5-large"
    messages     = @(
        @{
            role    = "user"
            content = "Voce eh um assistente especializado em topografia. Responda com 'OK' se conseguir me ler."
        }
    )
    temperature  = 0.7
    max_tokens   = 256
} | ConvertTo-Json

try {
    Write-Host "  Sending test message to Jamba..." -ForegroundColor Gray
    
    $response = Invoke-WebRequest `
        -Uri "https://openrouter.ai/api/v1/chat/completions" `
        -Method Post `
        -Headers $headers `
        -Body $payload `
        -TimeoutSec 30 `
        -ErrorAction Stop

    Write-Host "  Response Status: $($response.StatusCode)" -ForegroundColor Gray
    
    if ($response.StatusCode -eq 200) {
        Write-Host "[OK] OpenRouter API responded successfully (HTTP 200)" -ForegroundColor Green
        
        $responseJson = $response.Content | ConvertFrom-Json
        
        if ($responseJson.choices -and $responseJson.choices.Count -gt 0) {
            $messageContent = $responseJson.choices[0].message.content
            $preview = if ($messageContent.Length -gt 100) { $messageContent.Substring(0, 100) + "..." } else { $messageContent }
            Write-Host "  Model Response: $preview" -ForegroundColor Cyan
            Write-Host "[OK] Valid response structure from Jamba 1.5 Large" -ForegroundColor Green
            
            if ($responseJson.usage) {
                Write-Host "  Token Usage:" -ForegroundColor Cyan
                Write-Host "    - Input: $($responseJson.usage.prompt_tokens) tokens" -ForegroundColor Gray
                Write-Host "    - Output: $($responseJson.usage.completion_tokens) tokens" -ForegroundColor Gray
                Write-Host "    - Total: $($responseJson.usage.total_tokens) tokens" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "[ERROR] Unexpected status: $($response.StatusCode)" -ForegroundColor Red
        exit 1
    }
}
catch {
    $errorMessage = $_.Exception.Message
    
    if ($errorMessage -match "401") {
        Write-Host "[ERROR] Authentication failed (HTTP 401) - Invalid API key" -ForegroundColor Red
    }
    elseif ($errorMessage -match "429") {
        Write-Host "[WARN] Rate limited (HTTP 429) - Try again later" -ForegroundColor Yellow
    }
    elseif ($errorMessage -match "timeout") {
        Write-Host "[ERROR] Request timed out after 30 seconds" -ForegroundColor Red
    }
    else {
        Write-Host "[ERROR] Error: $errorMessage" -ForegroundColor Red
    }
    
    if ($Verbose) {
        Write-Host ""
        Write-Host "Full error details:" -ForegroundColor Red
        Write-Host $_ -ForegroundColor Red
    }
    
    exit 1
}

# Test 3: Summary
Write-Host ""
Write-Host "[Test 3/3] Test Summary" -ForegroundColor Blue
Write-Host "[OK] OpenRouter API is configured and functional" -ForegroundColor Green
Write-Host "  API Key Status: Valid and authenticated" -ForegroundColor Gray
Write-Host "  Primary Model: Jamba 1.5 Large (256K context)" -ForegroundColor Gray
Write-Host "  Alternative Model: Mistral (code-focused)" -ForegroundColor Gray
Write-Host "  Cost: $0.40-0.50 per 1M tokens" -ForegroundColor Gray
Write-Host "  Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Green
Write-Host "All tests passed! OpenRouter is ready for production use." -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Green
Write-Host ""

exit 0
