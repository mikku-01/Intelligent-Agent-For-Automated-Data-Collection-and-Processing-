# Git Upload Verification Script
# Run this before pushing to GitHub

Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "║              GIT UPLOAD VERIFICATION                               ║" -ForegroundColor White
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$allGood = $true

# Check 1: Verify .env is not going to be committed
Write-Host "🔍 Checking for sensitive files..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.env") {
        Write-Host "  ✅ .env file exists but is in .gitignore (GOOD)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ WARNING: .env file exists but NOT in .gitignore!" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  ⚠️  No .env file found (you'll need to create one)" -ForegroundColor Yellow
}

# Check 2: Verify .env.example exists
if (Test-Path ".env.example") {
    Write-Host "  ✅ .env.example exists (template for users)" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  .env.example not found (recommended to have)" -ForegroundColor Yellow
}

# Check 3: Check for database files
Write-Host "`n🔍 Checking for database files..." -ForegroundColor Yellow
$dbFiles = Get-ChildItem -Filter "*.db" -ErrorAction SilentlyContinue
if ($dbFiles.Count -eq 0) {
    Write-Host "  ✅ No .db files found (GOOD)" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Found $($dbFiles.Count) .db files (will be ignored by .gitignore)" -ForegroundColor Yellow
    $dbFiles | ForEach-Object { Write-Host "     - $($_.Name)" -ForegroundColor Gray }
}

# Check 4: Check for __pycache__
Write-Host "`n🔍 Checking for Python cache..." -ForegroundColor Yellow
$pycacheFiles = Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
if ($pycacheFiles.Count -eq 0) {
    Write-Host "  ✅ No __pycache__ directories found (GOOD)" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Found $($pycacheFiles.Count) __pycache__ directories (will be ignored)" -ForegroundColor Yellow
}

# Check 5: Check for venv directory
Write-Host "`n🔍 Checking for virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✅ venv directory exists but will be ignored (GOOD)" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  No venv directory found" -ForegroundColor Gray
}

# Check 6: Verify required files exist
Write-Host "`n🔍 Checking for required files..." -ForegroundColor Yellow
$requiredFiles = @("README.md", "requirements.txt", ".gitignore", "main.py", "demo.py")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file NOT FOUND!" -ForegroundColor Red
        $allGood = $false
    }
}

# Check 7: Count files that will be committed
Write-Host "`n📊 Project Statistics:" -ForegroundColor Yellow
$pythonFiles = (Get-ChildItem -Recurse -Filter "*.py" -Exclude "venv","__pycache__" | Measure-Object).Count
$mdFiles = (Get-ChildItem -Recurse -Filter "*.md" | Measure-Object).Count
$totalFiles = (Get-ChildItem -Recurse -File -Exclude "venv","__pycache__","*.db","*.log" | Measure-Object).Count

Write-Host "  Python files: $pythonFiles" -ForegroundColor White
Write-Host "  Documentation files: $mdFiles" -ForegroundColor White
Write-Host "  Total files to commit: ~$totalFiles" -ForegroundColor White

# Check 8: Check for API keys in code
Write-Host "`n🔍 Scanning for potential API keys in code..." -ForegroundColor Yellow
$suspiciousPatterns = @("sk-", "api_key", "secret_key", "password")
$foundIssues = $false

Get-ChildItem -Recurse -Filter "*.py" -Exclude "venv","__pycache__" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    foreach ($pattern in $suspiciousPatterns) {
        if ($content -match $pattern) {
            # Check if it's in a comment or example
            if ($content -notmatch "#.*$pattern" -and $content -notmatch "example.*$pattern" -and $content -notmatch "your.*$pattern") {
                Write-Host "  ⚠️  Found '$pattern' in $($_.Name)" -ForegroundColor Yellow
                $foundIssues = $true
            }
        }
    }
}

if (-not $foundIssues) {
    Write-Host "  ✅ No suspicious patterns found in code" -ForegroundColor Green
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                          SUMMARY" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "`n✅ " -NoNewline -ForegroundColor Green
    Write-Host "ALL CHECKS PASSED! Your project is ready for Git upload." -ForegroundColor White
    
    Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. git init" -ForegroundColor White
    Write-Host "  2. git add ." -ForegroundColor White
    Write-Host "  3. git commit -m 'Initial commit: Intelligent Agent'" -ForegroundColor White
    Write-Host "  4. git remote add origin <your-repo-url>" -ForegroundColor White
    Write-Host "  5. git push -u origin main`n" -ForegroundColor White
} else {
    Write-Host "`n⚠️  " -NoNewline -ForegroundColor Yellow
    Write-Host "SOME ISSUES FOUND. Please review above." -ForegroundColor White
    Write-Host "Fix the issues marked with ❌ before uploading.`n" -ForegroundColor White
}

Write-Host "💡 Tip: Read GIT_READY.md for detailed instructions`n" -ForegroundColor Cyan