#!/usr/bin/env powershell
# Quick test script for ATIVO REAL Backend

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "🚀 ATIVO REAL Backend Live Test" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""

$baseUrl = "https://ativo-real-backend.azurewebsites.net"
$tests = @(
    @{
        name = "Login Test"
        method = "POST"
        endpoint = "/api/auth/login"
        body = @{
            email = "topografo@bemreal.com"
            password = "password"
        } | ConvertTo-Json
    },
    @{
        name = "Get Projects"
        method = "GET"
        endpoint = "/api/projects"
        body = $null
    },
    @{
        name = "Get WMS Layers"
        method = "GET"
        endpoint = "/api/wms-layers"
        body = $null
    }
)

$results = @()

foreach ($test in $tests) {
    $uri = "$baseUrl$($test.endpoint)"
    Write-Host "Testing: $($test.name)" -ForegroundColor Yellow
    Write-Host "  URL: $uri" -ForegroundColor Gray
    
    try {
        $params = @{
            Uri = $uri
            Method = $test.method
            Headers = @{"Content-Type" = "application/json"}
            UseBasicParsing = $true
            ErrorAction = "Stop"
        }
        
        if ($test.body) {
            $params["Body"] = $test.body
        }
        
        $response = Invoke-WebRequest @params
        Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor Green
        $results += @{
            test = $test.name
            status = "PASS"
            code = $response.StatusCode
        }
    } catch {
        Write-Host "  ⚠️ Status: $(if($_.Exception.Response) { $_.Exception.Response.StatusCode.Value } else { 'No Response' })" -ForegroundColor Red
        $results += @{
            test = $test.name
            status = "FAIL"
            error = $_.Exception.Message
        }
    }
    Write-Host ""
}

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Green
$results | Format-Table -Property @{n="Test"; e={$_.test}}, @{n="Result"; e={$_.status}} -AutoSize

$passed = ($results | Where-Object { $_.status -eq "PASS" }).Count
$total = $results.Count

Write-Host ""
if ($passed -eq $total) {
    Write-Host "✅ ALL TESTS PASSED!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some tests failed. Check logs at:" -ForegroundColor Yellow
    Write-Host "   az functionapp log tail ativo-real-backend -g rg-ativo-real" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Backend URL: $baseUrl/api/" -ForegroundColor Cyan
Write-Host ""
