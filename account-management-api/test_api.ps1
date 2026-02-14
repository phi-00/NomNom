# Script de teste para a Account Management API

$baseUrl = "http://localhost:8000"

Write-Host "`nTestando Account Management API`n" -ForegroundColor Cyan

# 1. Testar endpoint raiz
Write-Host "1. Testando endpoint raiz (GET /)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method Get
    Write-Host "OK: $($response.message)" -ForegroundColor Green
    Write-Host "  Documentacao: $baseUrl$($response.docs)`n" -ForegroundColor Gray
} catch {
    Write-Host "Erro: $_`n" -ForegroundColor Red
}

# 2. Criar uma conta de teste
Write-Host "2. Criando uma conta de teste (POST /accounts/)..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$accountData = @{
    name = "Test User"
    email = "test.user.$timestamp@example.com"
    password = "password123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/accounts/" -Method Post -Body $accountData -ContentType "application/json"
    Write-Host "OK: Conta criada!" -ForegroundColor Green
    Write-Host "  ID: $($response.id)" -ForegroundColor Gray
    Write-Host "  Nome: $($response.name)" -ForegroundColor Gray
    Write-Host "  Email: $($response.email)" -ForegroundColor Gray
    Write-Host "  Data: $($response.created_at)`n" -ForegroundColor Gray
    
    $accountId = $response.id
    
    # 3. Buscar conta por ID
    Write-Host "3. Buscando conta (GET /accounts/{id})..." -ForegroundColor Yellow
    try {
        $getResponse = Invoke-RestMethod -Uri "$baseUrl/accounts/$accountId" -Method Get
        Write-Host "OK: Conta encontrada!" -ForegroundColor Green
        Write-Host "  Nome: $($getResponse.name)" -ForegroundColor Gray
        Write-Host "  Email: $($getResponse.email)`n" -ForegroundColor Gray
    } catch {
        Write-Host "Erro: $_`n" -ForegroundColor Red
    }
    
} catch {
    $errorMsg = $_
    Write-Host "Erro ao criar conta: $errorMsg`n" -ForegroundColor Red
}

# 4. Listar contas
Write-Host "4. Listando contas (GET /accounts/)..." -ForegroundColor Yellow
try {
    $listResponse = Invoke-RestMethod -Uri "$baseUrl/accounts/?limit=10" -Method Get
    Write-Host "OK: Encontradas $($listResponse.Count) conta(s)" -ForegroundColor Green
    foreach ($account in $listResponse) {
        Write-Host "  - $($account.name) ($($account.email))" -ForegroundColor Gray
    }
    Write-Host ""
} catch {
    Write-Host "Erro: $_`n" -ForegroundColor Red
}

Write-Host "`nTeste concluido!`n" -ForegroundColor Cyan
Write-Host "API disponivel em: $baseUrl`n" -ForegroundColor Green
