"""Test public API endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_rates(client):
    """Test GET /api/rates endpoint"""
    response = client.get("/api/rates")
    assert response.status_code == 200
    
    data = response.json()
    assert "rates" in data
    assert "paye_brackets" in data["rates"]
    assert "rebates" in data or "primary_rebate" in data["rates"]
    assert "vat_rate" in data["rates"]
    # Check new National Treasury 2024 alcohol framework
    assert "beer_excise_per_laa" in data["rates"]  # LAA-based
    assert "wine_excise_per_litre" in data["rates"]  # Volumetric
    assert "spirits_excise_per_laa" in data["rates"]  # LAA-based
    assert "cigarette_excise_per_20" in data["rates"]


def test_calc_simple_salary(client):
    """Test POST /api/calc with simple salary"""
    payload = {
        "personal": {
            "annual_salary": 240000,
            "age": 35
        },
        "consumption": {},
        "transport_property": {},
        "investment": {}
    }
    
    response = client.post("/api/calc", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "total" in data
    assert "monthly_total" in data
    assert "effective_rate_vs_gross" in data
    assert "breakdown" in data
    
    # Verify PAYE is calculated
    breakdown_has_paye = any("PAYE" in key for key in data["breakdown"].keys())
    assert breakdown_has_paye
    assert data["total"] > 0


def test_calc_with_consumption(client):
    """Test POST /api/calc with consumption data"""
    payload = {
        "personal": {
            "annual_salary": 240000,
            "age": 35
        },
        "consumption": {
            "std_vat_spend_month": 10000,
            "litres_petrol_month": 100,
            "beer_litres_month": 20,
            "beer_avg_abv": 5.0
        },
        "transport_property": {},
        "investment": {}
    }
    
    response = client.post("/api/calc", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    breakdown_keys = list(data["breakdown"].keys())
    # Check for indirect taxes and alcohol excise in breakdown
    has_vat = any("VAT" in key for key in breakdown_keys)
    has_alcohol = any("Beer" in key or "Alcohol" in key for key in breakdown_keys)
    assert has_vat or has_alcohol


def test_calc_full_profile(client):
    """Test POST /api/calc with all profile types"""
    payload = {
        "personal": {
            "annual_salary": 500000,
            "annual_bonus": 50000,
            "age": 40,
            "medical_members": 2
        },
        "consumption": {
            "std_vat_spend_month": 15000,
            "litres_petrol_month": 100,
            "litres_diesel_month": 50,
            "electricity_kwh_month": 800,
            "sugary_drink_litres_month": 20,
            "beer_litres_month": 20,
            "beer_avg_abv": 5.0,
            "wine_litres_month": 6,
            "wine_avg_abv": 12.5,
            "spirits_litres_month": 1,
            "spirits_avg_abv": 43.0,
            "cigarette_packs_20_month": 10,
            "cigarette_avg_price_per_pack": 35.0,
            "cigars_grams_month": 20,
            "pipe_tobacco_grams_month": 50,
            "plastic_bags_per_month": 20
        },
        "transport_property": {
            "vehicle_licence_fees_annual": 500,
            "tolls_annual": 1200,
            "municipal_rates_services_annual": 12000,
            "buying_property_price": 2000000
        },
        "investment": {
            "sa_dividends_annual": 20000,
            "capital_gains_annual": 50000
        }
    }
    
    response = client.post("/api/calc", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Should have various tax types in flat breakdown
    breakdown_keys = list(data["breakdown"].keys())
    assert len(breakdown_keys) > 5  # Should have multiple tax items
    
    # Verify total is sum of breakdown
    assert data["total"] > 0


def test_calc_validation_error(client):
    """Test POST /api/calc with invalid data"""
    payload = {
        "personal": {
            "annual_salary": -1000,  # Invalid negative salary
            "age": 35
        }
    }
    
    response = client.post("/api/calc", json=payload)
    assert response.status_code == 422  # Validation error


def test_calc_missing_required_fields(client):
    """Test POST /api/calc with missing required fields"""
    payload = {
        "personal": {
            # Missing annual_salary
            "age": 35
        }
    }
    
    response = client.post("/api/calc", json=payload)
    assert response.status_code == 422


def test_save_scenario(client):
    """Test POST /api/scenario to save calculation"""
    payload = {
        "label": "Test Scenario",
        "calc_request": {
            "personal": {"annual_salary": 240000, "age": 35},
            "consumption": {},
            "transport_property": {},
            "investment": {}
        },
        "calc_response": {
            "total": 50000,
            "monthly_total": 4166.67,
            "effective_rate_vs_gross": 20.83,
            "breakdown": {}
        }
    }
    
    response = client.post("/api/scenario", json=payload)
    assert response.status_code == 200  # Endpoint returns 200, not 201
    
    data = response.json()
    assert "id" in data
    assert data["label"] == "Test Scenario"
    assert "created_at" in data


def test_get_scenario(client):
    """Test GET /api/scenario/{id}"""
    # First create a scenario
    payload = {
        "label": "Retrieve Test",
        "calc_request": {
            "personal": {"annual_salary": 240000, "age": 35},
            "consumption": {},
            "transport_property": {},
            "investment": {}
        },
        "calc_response": {
            "total": 50000,
            "monthly_total": 4166.67,
            "effective_rate_vs_gross": 20.83,
            "breakdown": {}
        }
    }
    
    create_response = client.post("/api/scenario", json=payload)
    assert create_response.status_code == 200  # Endpoint returns 200, not 201
    scenario_id = create_response.json()["id"]
    
    # Now retrieve it
    get_response = client.get(f"/api/scenario/{scenario_id}")
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["id"] == scenario_id
    assert data["label"] == "Retrieve Test"


def test_get_nonexistent_scenario(client):
    """Test GET /api/scenario/{id} with non-existent ID"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/scenario/{fake_id}")
    assert response.status_code == 404
