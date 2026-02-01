# Test AI Endpoints - PowerShell Script
# Tests all 4 OpenRouter endpoints with valid JWT token

param(
    [string]$BaseUrl = "http://localhost:7071/api",
    [string]$AccessToken = "",
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\test_ai_endpoints.ps1 -AccessToken 'your-jwt-token'"
    Write-Host ""
    Write-Host "First, login to get access token:"
    Write-Host '  $response = Invoke-RestMethod -Uri "http://localhost:7071/api/auth/login" -Method Post -Body (@{email="admin@ativoreal.com"; password="Admin123!"} | ConvertTo-Json) -ContentType "application/json"'
    Write-Host '  $token = $response.access_token'
    Write-Host '  .\test_ai_endpoints.ps1 -AccessToken $token'
    exit 0
}

if (-not $AccessToken) {
    Write-Host "[ERROR] AccessToken is required" -ForegroundColor Red
    Write-Host "Run with -Help for usage instructions" -ForegroundColor Yellow
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $AccessToken"
    "Content-Type" = "application/json"
}

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "Testing AI Endpoints" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Chat
Write-Host "[Test 1/4] Testing /ai/chat..." -ForegroundColor Blue

$chatBody = @{
    messages = @(
        @{
            role = "user"
            content = "What is the best soil type for coffee plantations in Brazil?"
        }
    )
    model = "jamba-1.5-large"
    temperature = 0.7
    max_tokens = 500
} | ConvertTo-Json

try {
    $chatResponse = Invoke-RestMethod -Uri "$BaseUrl/ai/chat" -Method Post -Headers $headers -Body $chatBody
    
    if ($chatResponse.choices) {
        Write-Host "[OK] Chat endpoint working" -ForegroundColor Green
        $content = $chatResponse.choices[0].message.content
        Write-Host "  Response preview: $($content.Substring(0, [Math]::Min(100, $content.Length)))..." -ForegroundColor Gray
        
        if ($chatResponse.usage) {
            Write-Host "  Tokens used: $($chatResponse.usage.total_tokens)" -ForegroundColor Gray
        }
    } else {
        Write-Host "[WARN] Unexpected response format" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[ERROR] Chat endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: Analyze Topography
Write-Host "[Test 2/4] Testing /ai/analyze-topography..." -ForegroundColor Blue

$analyzeBody = @{
    prompt = "Analyze a 50 hectare property with rolling hills and a small river"
    context = "Located in Minas Gerais state, Brazil"
} | ConvertTo-Json

try {
    $analyzeResponse = Invoke-RestMethod -Uri "$BaseUrl/ai/analyze-topography" -Method Post -Headers $headers -Body $analyzeBody
    
    if ($analyzeResponse.analysis) {
        Write-Host "[OK] Topography analysis endpoint working" -ForegroundColor Green
        $analysis = $analyzeResponse.analysis
        Write-Host "  Analysis preview: $($analysis.Substring(0, [Math]::Min(100, $analysis.Length)))..." -ForegroundColor Gray
    } else {
        Write-Host "[WARN] Unexpected response format" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[ERROR] Analyze endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Generate Report
Write-Host "[Test 3/4] Testing /ai/generate-report..." -ForegroundColor Blue

$reportBody = @{
    data = @{
        area_ha = 75.5
        soil_type = "Latossolo Vermelho"
        elevation_min = 450
        elevation_max = 620
        water_sources = @("Rio Verde", "3 springs")
        forest_area_ha = 15.2
    }
} | ConvertTo-Json

try {
    $reportResponse = Invoke-RestMethod -Uri "$BaseUrl/ai/generate-report" -Method Post -Headers $headers -Body $reportBody
    
    if ($reportResponse.report) {
        Write-Host "[OK] Report generation endpoint working" -ForegroundColor Green
        $report = $reportResponse.report
        Write-Host "  Report preview: $($report.Substring(0, [Math]::Min(100, $report.Length)))..." -ForegroundColor Gray
    } else {
        Write-Host "[WARN] Unexpected response format" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[ERROR] Report endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Validate Geometry
Write-Host "[Test 4/4] Testing /ai/validate-geometry..." -ForegroundColor Blue

$validateBody = @{
    description = "Property bounded by coordinates: (-47.123, -21.456), (-47.234, -21.456), (-47.234, -21.567), (-47.123, -21.567)"
} | ConvertTo-Json

try {
    $validateResponse = Invoke-RestMethod -Uri "$BaseUrl/ai/validate-geometry" -Method Post -Headers $headers -Body $validateBody
    
    if ($validateResponse.PSObject.Properties.Name -contains "is_valid") {
        Write-Host "[OK] Geometry validation endpoint working" -ForegroundColor Green
        Write-Host "  Valid: $($validateResponse.is_valid)" -ForegroundColor Gray
        Write-Host "  Confidence: $($validateResponse.confidence)" -ForegroundColor Gray
        
        if ($validateResponse.geometric_type) {
            Write-Host "  Type: $($validateResponse.geometric_type)" -ForegroundColor Gray
        }
    } else {
        Write-Host "[WARN] Unexpected response format" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[ERROR] Validate endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "Test completed!" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""
