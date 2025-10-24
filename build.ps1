# BleedRate PowerShell Build Script
# Usage: .\build.ps1 <command>
# Example: .\build.ps1 dev

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "🩸 BleedRate Build Commands" -ForegroundColor Red
    Write-Host ""
    Write-Host "Development:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 install          Install dependencies"
    Write-Host "  .\build.ps1 dev              Run development server"
    Write-Host "  .\build.ps1 lint             Check code style"
    Write-Host "  .\build.ps1 format           Format code"
    Write-Host ""
    Write-Host "Testing:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 test             Run tests with coverage"
    Write-Host "  .\build.ps1 test-fast        Quick test (stop at first failure)"
    Write-Host "  .\build.ps1 test-verbose     Detailed test output with HTML report"
    Write-Host "  .\build.ps1 test-coverage    Generate coverage report"
    Write-Host ""
    Write-Host "Deployment:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 switch-to-dev    Switch to dev branch"
    Write-Host "  .\build.ps1 switch-to-main   Switch to main branch"
    Write-Host "  .\build.ps1 deploy-dev       Deploy to development"
    Write-Host "  .\build.ps1 deploy-prod      Deploy to production"
    Write-Host ""
    Write-Host "Maintenance:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 clean            Clean cache files"
}

function Install-Dependencies {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
    python -m pip install -r requirements.txt
}

function Start-Dev {
    Write-Host "🚀 Starting development server..." -ForegroundColor Cyan
    uvicorn app.main:app --reload --port 8000
}

function Run-Lint {
    Write-Host "🔍 Checking code style..." -ForegroundColor Cyan
    ruff check .
    if ($LASTEXITCODE -eq 0) {
        black --check .
    }
}

function Run-Format {
    Write-Host "✨ Formatting code..." -ForegroundColor Cyan
    black .
    ruff check . --fix
}

function Run-Tests {
    Write-Host "🧪 Running tests..." -ForegroundColor Cyan
    pytest tests/ -v --cov=app --cov-report=term-missing
}

function Run-TestsFast {
    Write-Host "⚡ Running fast tests..." -ForegroundColor Cyan
    pytest tests/ -x -q
    Write-Host "⚡ Fast mode: stops at first failure" -ForegroundColor Gray
}

function Run-TestsVerbose {
    Write-Host "🧪 Running detailed tests..." -ForegroundColor Cyan
    pytest tests/ -vv --cov=app --cov-report=term-missing --cov-report=html
    Write-Host "📊 Detailed output with HTML coverage report" -ForegroundColor Gray
}

function Run-TestsCoverage {
    Write-Host "📊 Generating coverage report..." -ForegroundColor Cyan
    pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
    Write-Host "📊 Coverage report generated in htmlcov/index.html" -ForegroundColor Green
    Write-Host "Opening coverage report..." -ForegroundColor Gray
    Start-Process "htmlcov/index.html"
}

function Clean-Cache {
    Write-Host "🧹 Cleaning cache files..." -ForegroundColor Cyan
    
    # Remove __pycache__ directories
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
    
    # Remove .pyc files
    Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
    
    # Remove test/coverage artifacts
    if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }
    if (Test-Path ".coverage") { Remove-Item -Force ".coverage" }
    if (Test-Path "htmlcov") { Remove-Item -Recurse -Force "htmlcov" }
    if (Test-Path ".ruff_cache") { Remove-Item -Recurse -Force ".ruff_cache" }
    
    Write-Host "✅ Cleaned up cache files" -ForegroundColor Green
}

function Switch-ToDev {
    Write-Host "🔄 Switching to dev branch..." -ForegroundColor Cyan
    git checkout dev
    if ($LASTEXITCODE -eq 0) {
        git pull origin dev
        Write-Host "✅ Now on dev branch" -ForegroundColor Green
    }
}

function Switch-ToMain {
    Write-Host "🔄 Switching to main branch..." -ForegroundColor Cyan
    git checkout main
    if ($LASTEXITCODE -eq 0) {
        git pull origin main
        Write-Host "✅ Now on main branch" -ForegroundColor Green
    }
}

function Deploy-Dev {
    Write-Host "🚀 Deploying to DEVELOPMENT environment..." -ForegroundColor Cyan
    git checkout dev
    if ($LASTEXITCODE -eq 0) {
        git push origin dev
        Write-Host "✅ Development deployment triggered!" -ForegroundColor Green
        Write-Host "🔗 Check Railway dashboard for deployment status" -ForegroundColor Gray
    }
}

function Deploy-Prod {
    Write-Host "🚀 Deploying to PRODUCTION environment..." -ForegroundColor Cyan
    git checkout main
    if ($LASTEXITCODE -eq 0) {
        git push origin main
        Write-Host "✅ Production deployment triggered!" -ForegroundColor Green
        Write-Host "🔗 Check Railway dashboard for deployment status" -ForegroundColor Gray
    }
}

# Command dispatcher
switch ($Command.ToLower()) {
    "install" { Install-Dependencies }
    "dev" { Start-Dev }
    "lint" { Run-Lint }
    "format" { Run-Format }
    "test" { Run-Tests }
    "test-fast" { Run-TestsFast }
    "test-verbose" { Run-TestsVerbose }
    "test-coverage" { Run-TestsCoverage }
    "clean" { Clean-Cache }
    "switch-to-dev" { Switch-ToDev }
    "switch-to-main" { Switch-ToMain }
    "deploy-dev" { Deploy-Dev }
    "deploy-prod" { Deploy-Prod }
    "help" { Show-Help }
    default { 
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
