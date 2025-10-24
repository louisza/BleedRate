.PHONY: install dev lint format test clean deploy-dev deploy-prod promote-to-prod switch-to-dev switch-to-main

install:
	python -m pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	ruff check . && black --check .

format:
	black . && ruff check . --fix

test:
	pytest -q --cov=app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

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
