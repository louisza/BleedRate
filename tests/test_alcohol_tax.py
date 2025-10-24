"""Test alcohol tax calculations"""
import pytest
from pathlib import Path
from app.domain.rates import TaxRates
from app.domain.profiles import ConsumptionProfile
from app.domain.calculators import AlcoholTaxCalculator


@pytest.fixture
def rates():
    """Load tax rates"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    return TaxRates.load_from_yaml(rates_path)


@pytest.fixture
def calculator(rates):
    """Create alcohol tax calculator"""
    return AlcoholTaxCalculator(rates)


def test_beer_excise_calculation(calculator):
    """Test beer excise calculation - LAA-based
    
    Official rate: R121.41 per litre of absolute alcohol (LAA)
    Formula: Litres × (ABV% / 100) × R121.41 × 12 months
    """
    profile = ConsumptionProfile(
        beer_litres_month=20.0,  # 20 litres per month
        beer_avg_abv=5.0  # 5% ABV
    )
    
    result = calculator.calculate(profile)
    
    # 20L × 5% = 1 LAA per month
    # 1 LAA × R121.41 = R121.41 per month
    # × 12 = R1,456.92 per year
    assert "Beer Excise" in result
    laa_per_month = 20 * (5.0 / 100)
    expected_annual = laa_per_month * 121.41 * 12
    assert result["Beer Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_wine_excise_calculation(calculator):
    """Test wine excise calculation - Volumetric
    
    Official rate: R4.96 per litre of wine (NOT LAA-based)
    Formula: Litres × R4.96 × 12 months
    """
    profile = ConsumptionProfile(
        wine_litres_month=6.0,  # 6 litres per month (~8 bottles)
        wine_avg_abv=12.5  # 12.5% ABV (NOT used - volumetric rate)
    )
    
    result = calculator.calculate(profile)
    
    assert "Wine Excise" in result
    # 6L × R4.96 = R29.76 per month
    # × 12 = R357.12 per year
    expected_annual = 6 * 4.96 * 12
    assert result["Wine Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_spirits_excise_calculation(calculator):
    """Test spirits excise calculation"""
    profile = ConsumptionProfile(
        spirits_litres_month=1.0,  # 1 litre per month
        spirits_avg_abv=43.0  # 43% ABV
    )
    
    result = calculator.calculate(profile)
    
    assert "Spirits Excise" in result
    expected_annual = 1 * (43.0 / 100) * 249.20 * 12
    assert result["Spirits Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_mixed_alcohol(calculator):
    """Test calculation with multiple alcohol types"""
    profile = ConsumptionProfile(
        beer_litres_month=20.0,
        beer_avg_abv=5.0,
        wine_litres_month=6.0,
        wine_avg_abv=12.5,
        spirits_litres_month=1.0,
        spirits_avg_abv=43.0
    )
    
    result = calculator.calculate(profile)
    
    assert len(result) == 3
    assert "Beer Excise" in result
    assert "Wine Excise" in result
    assert "Spirits Excise" in result


def test_zero_alcohol(calculator):
    """Test with no alcohol consumption"""
    profile = ConsumptionProfile()
    
    result = calculator.calculate(profile)
    
    assert len(result) == 0


def test_extreme_abv_edge_cases(calculator):
    """Test with extreme ABV values"""
    # 0% ABV (non-alcoholic) - beer with LAA calculation
    profile_zero = ConsumptionProfile(
        beer_litres_month=20.0,
        beer_avg_abv=0.0  # 0% ABV = 0 LAA
    )
    result_zero = calculator.calculate(profile_zero)
    # 0% ABV = 0 LAA = R0 excise (LAA-based calculation)
    expected_beer = 20.0 * (0.0 / 100) * 121.41 * 12
    assert result_zero["Beer Excise"] == pytest.approx(expected_beer, rel=0.01)
    
    # 100% ABV (pure alcohol - theoretical) - spirits
    profile_max = ConsumptionProfile(
        spirits_litres_month=1.0,
        spirits_avg_abv=100.0
    )
    result_max = calculator.calculate(profile_max)
    expected = 1.0 * 249.20 * 12  # Full LAA rate
    assert result_max["Spirits Excise"] == pytest.approx(expected, rel=0.01)
