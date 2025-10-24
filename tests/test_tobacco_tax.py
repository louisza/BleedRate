"""Test tobacco tax calculations"""
import pytest
from pathlib import Path
from app.domain.rates import TaxRates
from app.domain.profiles import ConsumptionProfile
from app.domain.calculators import TobaccoTaxCalculator


@pytest.fixture
def rates():
    """Load tax rates"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    return TaxRates.load_from_yaml(rates_path)


@pytest.fixture
def calculator(rates):
    """Create tobacco tax calculator"""
    return TobaccoTaxCalculator(rates)


def test_cigarette_specific_excise(calculator):
    """Test cigarette excise using specific rate"""
    # Low-priced cigarettes where specific rate dominates
    profile = ConsumptionProfile(
        cigarette_packs_20_month=10,  # 10 packs per month
        cigarette_avg_price_per_pack=25.0  # R25 per pack (low price)
    )
    
    result = calculator.calculate(profile)
    
    assert "Cigarette Excise" in result
    # Specific: 10 packs × R18.22 = R182.20/month × 12 = R2,186.40
    # Ad valorem: 10 × R25 × 30% = R75/month × 12 = R900
    # Max(2186.40, 900) = R2,186.40
    expected_annual = 10 * 18.22 * 12
    assert result["Cigarette Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_cigarette_ad_valorem_excise(calculator):
    """Test cigarette excise using ad valorem rate"""
    # Premium cigarettes where ad valorem dominates
    profile = ConsumptionProfile(
        cigarette_packs_20_month=10,  # 10 packs per month
        cigarette_avg_price_per_pack=100.0  # R100 per pack (premium)
    )
    
    result = calculator.calculate(profile)
    
    assert "Cigarette Excise" in result
    # Specific: 10 × R18.22 = R182.20/month × 12 = R2,186.40
    # Ad valorem: 10 × R100 × 30% = R300/month × 12 = R3,600
    # Max(2186.40, 3600) = R3,600
    expected_annual = 10 * 100.0 * 0.30 * 12
    assert result["Cigarette Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_cigars_excise(calculator):
    """Test cigars excise calculation"""
    profile = ConsumptionProfile(
        cigars_grams_month=50.0  # 50 grams per month
    )
    
    result = calculator.calculate(profile)
    
    assert "Cigar Excise" in result
    # 50g × R10.96 = R548/month × 12 = R6,576
    expected_annual = 50.0 * 10.96 * 12
    assert result["Cigar Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_pipe_tobacco_excise(calculator):
    """Test pipe tobacco excise calculation"""
    profile = ConsumptionProfile(
        pipe_tobacco_grams_month=100.0  # 100 grams per month
    )
    
    result = calculator.calculate(profile)
    
    assert "Pipe Tobacco Excise" in result
    # 100g × R5.44 = R544/month × 12 = R6,528
    expected_annual = 100.0 * 5.44 * 12
    assert result["Pipe Tobacco Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_mixed_tobacco(calculator):
    """Test calculation with multiple tobacco types"""
    profile = ConsumptionProfile(
        cigarette_packs_20_month=10,
        cigarette_avg_price_per_pack=35.0,
        cigars_grams_month=20.0,
        pipe_tobacco_grams_month=50.0
    )
    
    result = calculator.calculate(profile)
    
    assert len(result) == 3
    assert "Cigarette Excise" in result
    assert "Cigar Excise" in result
    assert "Pipe Tobacco Excise" in result


def test_zero_tobacco(calculator):
    """Test with no tobacco consumption"""
    profile = ConsumptionProfile()
    
    result = calculator.calculate(profile)
    
    assert len(result) == 0


def test_cigarette_breakeven_point(calculator):
    """Test cigarette price where specific equals ad valorem"""
    # Breakeven: specific = ad_valorem
    # R18.22 = price × 30%
    # price = R18.22 / 0.30 = ~R60.73
    
    profile_below = ConsumptionProfile(
        cigarette_packs_20_month=10,
        cigarette_avg_price_per_pack=60.0  # Below breakeven
    )
    result_below = calculator.calculate(profile_below)
    specific_result = 10 * 18.22 * 12
    
    profile_above = ConsumptionProfile(
        cigarette_packs_20_month=10,
        cigarette_avg_price_per_pack=61.0  # Above breakeven
    )
    result_above = calculator.calculate(profile_above)
    ad_valorem_result = 10 * 61.0 * 0.30 * 12
    
    # Below breakeven should use specific rate
    assert result_below["Cigarette Excise"] == pytest.approx(specific_result, rel=0.01)
    # Above breakeven should use ad valorem rate
    assert result_above["Cigarette Excise"] == pytest.approx(ad_valorem_result, rel=0.01)
