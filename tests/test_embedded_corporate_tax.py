"""Test embedded corporate tax calculations"""
import pytest
from pathlib import Path
from app.domain.rates import TaxRates
from app.domain.profiles import ConsumptionProfile
from app.domain.calculators import EmbeddedCorporateTaxCalculator


@pytest.fixture
def rates():
    """Load tax rates"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    return TaxRates.load_from_yaml(rates_path)


@pytest.fixture
def calculator(rates):
    """Create embedded corporate tax calculator"""
    return EmbeddedCorporateTaxCalculator(rates)


def test_embedded_tax_basic_calculation(calculator):
    """Test basic embedded corporate tax calculation"""
    profile = ConsumptionProfile(
        std_vat_spend_month=10000.0  # R10k/month = R120k/year
    )
    
    result = calculator.calculate(profile)
    
    # Should calculate 12% of R120k = R14,400
    total_embedded = sum(result.values())
    assert total_embedded == pytest.approx(14400.0, rel=0.01)
    
    # Check all components are present
    assert "Corporate Income Tax (embedded)" in result
    assert "SDL/UIF Employer Contribution (embedded)" in result
    assert "Tax Administration Costs (embedded)" in result
    assert "Regulatory Compliance Costs (embedded)" in result
    assert "Supply Chain Tax Cascade (embedded)" in result


def test_embedded_tax_component_breakdown(calculator):
    """Test component breakdown matches expected proportions"""
    profile = ConsumptionProfile(
        std_vat_spend_month=10000.0
    )
    
    result = calculator.calculate(profile)
    total = sum(result.values())
    
    # Verify proportions
    cit = result["Corporate Income Tax (embedded)"]
    assert cit == pytest.approx(total * 0.40, rel=0.01)  # 40% of total
    
    sdl_uif = result["SDL/UIF Employer Contribution (embedded)"]
    assert sdl_uif == pytest.approx(total * 0.15, rel=0.01)  # 15% of total
    
    admin = result["Tax Administration Costs (embedded)"]
    assert admin == pytest.approx(total * 0.10, rel=0.01)  # 10% of total
    
    regulatory = result["Regulatory Compliance Costs (embedded)"]
    assert regulatory == pytest.approx(total * 0.20, rel=0.01)  # 20% of total
    
    cascade = result["Supply Chain Tax Cascade (embedded)"]
    assert cascade == pytest.approx(total * 0.15, rel=0.01)  # 15% of total


def test_embedded_tax_zero_spending(calculator):
    """Test with no spending"""
    profile = ConsumptionProfile(
        std_vat_spend_month=0.0
    )
    
    result = calculator.calculate(profile)
    assert len(result) == 0


def test_get_total_embedded(calculator):
    """Test get_total_embedded helper method"""
    profile = ConsumptionProfile(
        std_vat_spend_month=5000.0  # R5k/month = R60k/year
    )
    
    total = calculator.get_total_embedded(profile)
    
    # Should be 12% of R60k = R7,200
    assert total == pytest.approx(7200.0, rel=0.01)


def test_calculate_by_industry(calculator):
    """Test industry-specific calculation"""
    spending = {
        "groceries": 30000.0,      # Retail: 10%
        "restaurants": 20000.0,    # Labour-intensive: 17%
        "electronics": 15000.0,    # Manufacturing: 13%
        "online_shopping": 10000.0, # Technology: 8%
    }
    
    result = calculator.calculate_by_industry(spending)
    
    # Check all categories present
    assert "Embedded Tax: Groceries" in result
    assert "Embedded Tax: Restaurants" in result
    assert "Embedded Tax: Electronics" in result
    assert "Embedded Tax: Online_Shopping" in result
    
    # Verify calculations
    assert result["Embedded Tax: Groceries"] == pytest.approx(30000 * 0.10, rel=0.01)
    assert result["Embedded Tax: Restaurants"] == pytest.approx(20000 * 0.17, rel=0.01)
    assert result["Embedded Tax: Electronics"] == pytest.approx(15000 * 0.13, rel=0.01)
    assert result["Embedded Tax: Online_Shopping"] == pytest.approx(10000 * 0.08, rel=0.01)


def test_embedded_rates_structure(calculator):
    """Test that embedded rate structure is complete"""
    rates = calculator.embedded_rates
    
    # Check all expected industries present
    assert "labour_intensive" in rates
    assert "manufacturing" in rates
    assert "retail" in rates
    assert "services" in rates
    assert "technology" in rates
    assert "weighted_average" in rates
    
    # Check rates are reasonable (between 5% and 20%)
    for industry, rate in rates.items():
        assert 0.05 <= rate <= 0.20, f"{industry} rate {rate} outside reasonable range"


def test_component_weights_sum_to_one(calculator):
    """Test that component weights sum to 100%"""
    weights = calculator.component_weights
    total_weight = sum(weights.values())
    
    assert total_weight == pytest.approx(1.0, rel=0.01)


def test_realistic_scenario(calculator):
    """Test with realistic middle-class spending"""
    profile = ConsumptionProfile(
        std_vat_spend_month=15000.0  # R15k/month VAT spending
    )
    
    result = calculator.calculate(profile)
    total = sum(result.values())
    
    # R15k × 12 = R180k annual spending
    # 12% embedded = R21,600
    assert total == pytest.approx(21600.0, rel=0.01)
    
    # CIT component should be largest (40%)
    cit = result["Corporate Income Tax (embedded)"]
    assert cit == max(result.values())
    assert cit == pytest.approx(8640.0, rel=0.01)  # 40% of R21,600


def test_high_income_scenario(calculator):
    """Test with high spending profile"""
    profile = ConsumptionProfile(
        std_vat_spend_month=50000.0  # R50k/month
    )
    
    total = calculator.get_total_embedded(profile)
    
    # R50k × 12 = R600k annual
    # 12% = R72,000
    assert total == pytest.approx(72000.0, rel=0.01)


def test_calculate_by_industry_unknown_category(calculator):
    """Test that unknown categories default to weighted average"""
    spending = {
        "unknown_category": 10000.0,
    }
    
    result = calculator.calculate_by_industry(spending)
    
    # Should use weighted_average rate (12%)
    assert result["Embedded Tax: Unknown_Category"] == pytest.approx(10000 * 0.12, rel=0.01)


def test_calculate_by_industry_zero_spending(calculator):
    """Test that zero spending categories are skipped"""
    spending = {
        "groceries": 10000.0,
        "restaurants": 0.0,  # Zero spending
        "clothing": -100.0,  # Negative (invalid)
    }
    
    result = calculator.calculate_by_industry(spending)
    
    # Only groceries should appear
    assert "Embedded Tax: Groceries" in result
    assert "Embedded Tax: Restaurants" not in result
    assert "Embedded Tax: Clothing" not in result
