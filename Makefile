.PHONY: install dev lint format test test-verbose test-fast test-coverage test-watch test-parallel clean deploy-dev deploy-prod promote-to-prod switch-to-dev switch-to-main

install:
	python -m pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	ruff check . && black --check .

format:
	black . && ruff check . --fix

# Testing commands
test:
	pytest tests/ -v --cov=app --cov-report=term-missing

test-verbose:
	pytest tests/ -vv --cov=app --cov-report=term-missing --cov-report=html
	@echo "📊 Detailed output with HTML coverage report"

test-fast:
	pytest tests/ -x -q
	@echo "⚡ Fast mode: stops at first failure"

test-coverage:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report generated in htmlcov/index.html"
	@echo "Opening coverage report..."
	@open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null || echo "Open htmlcov/index.html manually"

test-watch:
	@echo "👀 Running tests in watch mode (auto-runs on file changes)..."
	@echo "Press Ctrl+C to stop"
	ptw -- tests/ -v

test-parallel:
	pytest tests/ -n auto --cov=app -v
	@echo "⚡ Tests ran in parallel across all CPU cores"

test-ci:
	pytest tests/ --cov=app --cov-report=xml --cov-report=term --cov-fail-under=70 -v
	@echo "✅ CI mode: enforces minimum 70% coverage"

test-specific:
	@read -p "Enter test file or function path: " test_path; \
	pytest $$test_path -vv

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .ruff_cache
	@echo "🧹 Cleaned up cache files"

# Deployment commands
deploy-dev:
	@echo "🚀 Deploying to DEVELOPMENT environment..."
	@git checkout dev
	@git push origin dev
	@echo "✅ Development deployment triggered!"
	@echo "🔗 Check Railway dashboard for deployment status"

deploy-prod:
	@echo "🚀 Deploying to PRODUCTION environment..."
	@git checkout main
	@git push origin main
	@echo "✅ Production deployment triggered!"
	@echo "🔗 Check Railway dashboard for deployment status"

promote-to-prod:
	@echo "📦 Promoting dev to production..."
	@echo "⚠️  This will merge dev into main and deploy to production"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		git checkout main && \
		git merge dev && \
		git push origin main && \
		git checkout dev && \
		echo "✅ Successfully promoted to production!"; \
	else \
		echo "❌ Promotion cancelled"; \
	fi

switch-to-dev:
	@echo "🔄 Switching to dev branch..."
	@git checkout dev
	@git pull origin dev
	@echo "✅ Now on dev branch"

switch-to-main:
	@echo "🔄 Switching to main branch..."
	@git checkout main
	@git pull origin main
	@echo "✅ Now on main branch"
