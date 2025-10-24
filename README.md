# 💸 How Much Goes to Government? - SA Tax Calculator

A production-ready FastAPI application that shows exactly how much of your money flows to the South African government through various taxes, levies, and hidden charges.

## Features

- � **Complete money flow tracking** - See every Rand that goes to government (PAYE, VAT, fuel levies, sin taxes, etc.)
- 💡 **Interactive tooltips** - Hover over any category to see exactly how your money flows to government
- 🍺 **Alcohol excise tracking** - Beer/wine/spirits with ABV calculations showing government's cut
- 🚬 **Tobacco excise tracking** - Cigarettes, cigars, pipe tobacco - see the sin tax you pay
- 💰 **Investment taxes** - Track dividends tax and capital gains going to SARS
- 🏠 **Property transfer duty** - One-time government charge on property purchases
- � **Vehicle import duty** - See 25% duty on imported vehicles flowing to government
- 🏭 **Hidden embedded taxes** - Reveals ~12% corporate taxes passed through prices
- 📈 **Clear visualizations** - Charts showing your money flowing to government coffers
- 📤 **Export capabilities** - Save your government money flow analysis to CSV/JSON
- ⚙️ **Admin interface** - Update tax rates as government changes them

## Requirements

- Python ≥ 3.11

## Quick Start

### 1. Clone and Setup

```powershell
cd sa-tax-footprint
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
copy .env.example .env
```

Edit `.env` with your settings.

### 3. Run Development Server

```powershell
uvicorn app.main:app --reload --port 8000
```

Or use the Makefile:

```powershell
make dev
```

### 4. Access the Application

Open your browser to: `http://localhost:8000`

## Project Structure

```
sa-tax-footprint/
├── app/
│   ├── domain/          # Business logic (calculators, rates, profiles)
│   ├── api/             # REST API endpoints
│   ├── views/           # Server-rendered pages
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # CSS and JavaScript
├── data/               # Tax rates configuration (YAML)
├── db/                 # Database models and SQLite file
├── tests/              # Unit and integration tests
└── scripts/            # Utility scripts

```

## Development

### Run Tests

```powershell
pytest
```

Or with coverage:

```powershell
make test
```

### Lint and Format

```powershell
make lint      # Check code quality
make format    # Auto-format code
```

## Docker Deployment

### Build and Run

```powershell
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/calc` - Calculate tax breakdown
- `GET /api/rates` - View current tax rates
- `POST /api/scenario` - Save calculation scenario
- `GET /admin/rates` - Admin: Edit tax rates
- `POST /admin/rates` - Admin: Update tax rates

## Tax Rates

All tax rates are configurable via `data/tax_rates.yml`. The admin interface provides a web-based editor with validation.

## License

MIT

## Contributing

Contributions welcome! Please ensure all tests pass before submitting PRs.
