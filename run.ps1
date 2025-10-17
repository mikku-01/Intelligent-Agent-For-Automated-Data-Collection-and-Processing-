# Intelligent Agent Project - Common Commands
# Run these commands to perform common tasks

# Setup and Installation
Write-Host "`n=== Intelligent Agent Project - Command Reference ===" -ForegroundColor Cyan
Write-Host "`nCommon Commands:`n" -ForegroundColor Yellow

$commands = @"
1. SETUP
   python setup.py

2. INSTALL DEPENDENCIES
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm

3. RUN DEMO (No API keys needed)
   python demo.py

4. RUN TESTS
   pytest tests/ -v

5. RUN AGENT
   python test_run.py

6. CHECK CODE QUALITY
   pytest tests/ --cov=.

7. VIEW LOGS
   Get-Content logs/agent.log -Tail 50

8. CLEAN PROJECT
   Remove-Item -Recurse -Force __pycache__, *.pyc, .pytest_cache, logs/*.log

9. CREATE VIRTUAL ENVIRONMENT
   python -m venv venv
   .\venv\Scripts\activate

10. DEACTIVATE VIRTUAL ENVIRONMENT
    deactivate

"@

Write-Host $commands -ForegroundColor White

Write-Host "`nQuick Actions:`n" -ForegroundColor Yellow

function Show-Menu {
    param (
        [string]$Title = 'Intelligent Agent - Quick Actions'
    )
    Write-Host "================ $Title ================" -ForegroundColor Cyan
    Write-Host "1: Run Demo (Mock Data)"
    Write-Host "2: Run Setup"
    Write-Host "3: Install Dependencies"
    Write-Host "4: Run Tests"
    Write-Host "5: View Recent Logs"
    Write-Host "6: Clean Project"
    Write-Host "Q: Quit"
    Write-Host "======================================" -ForegroundColor Cyan
}

do {
    Show-Menu
    $selection = Read-Host "`nPlease make a selection"
    switch ($selection) {
        '1' {
            Write-Host "`nRunning demo..." -ForegroundColor Green
            python demo.py
        }
        '2' {
            Write-Host "`nRunning setup..." -ForegroundColor Green
            python setup.py
        }
        '3' {
            Write-Host "`nInstalling dependencies..." -ForegroundColor Green
            pip install -r requirements.txt
            python -m spacy download en_core_web_sm
        }
        '4' {
            Write-Host "`nRunning tests..." -ForegroundColor Green
            pytest tests/ -v
        }
        '5' {
            Write-Host "`nRecent logs:" -ForegroundColor Green
            if (Test-Path "logs/agent.log") {
                Get-Content logs/agent.log -Tail 20
            } else {
                Write-Host "No logs found" -ForegroundColor Yellow
            }
        }
        '6' {
            Write-Host "`nCleaning project..." -ForegroundColor Green
            Get-ChildItem -Path . -Include __pycache__,*.pyc,.pytest_cache -Recurse | Remove-Item -Force -Recurse
            if (Test-Path "logs/*.log") {
                Remove-Item logs/*.log -Force
            }
            Write-Host "Project cleaned!" -ForegroundColor Green
        }
        'q' {
            return
        }
    }
    pause
} until ($selection -eq 'q')