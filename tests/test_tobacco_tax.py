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
    # Specific: 10 packs × R22.81 = R228.10/month × 12 = R2,737.20 [2026/27]
    # Ad valorem: 10 × R25 × 30% = R75/month × 12 = R900
    # Max(2737.20, 900) = R2,737.20
    expected_annual = 10 * 22.81 * 12
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
    # Specific: 10 × R22.81 = R228.10/month × 12 = R2,737.20
    # Ad valorem: 10 × R100 × 30% = R300/month × 12 = R3,600
    # Max(2737.20, 3600) = R3,600
    expected_annual = 10 * 100.0 * 0.30 * 12
    assert result["Cigarette Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_cigars_excise(calculator):
    """Test cigars excise calculation [2026/27: R138.96 per 23g = R6.04/g]"""
    profile = ConsumptionProfile(
        cigars_grams_month=50.0  # 50 grams per month
    )

    result = calculator.calculate(profile)

    assert "Cigar Excise" in result
    # 2026/27: R138.96/23g ≈ R6.0417/g
    # 50g × R6.0417 = R302.09/month × 12 = R3,625.04
    cigar_rate_per_gram = 138.96 / 23
    expected_annual = 50.0 * cigar_rate_per_gram * 12
    assert result["Cigar Excise"] == pytest.approx(expected_annual, rel=0.01)


def test_pipe_tobacco_excise(calculator):
    """Test pipe tobacco excise calculation [2026/27: R8.31 per 25g = R0.3324/g]"""
    profile = ConsumptionProfile(
        pipe_tobacco_grams_month=100.0  # 100 grams per month
    )

    result = calculator.calculate(profile)

    assert "Pipe Tobacco Excise" in result
    # 2026/27: R8.31/25g = R0.3324/g
    # 100g × R0.3324 = R33.24/month × 12 = R398.88
    pipe_rate_per_gram = 8.31 / 25
    expected_annual = 100.0 * pipe_rate_per_gram * 12
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
    """Test cigarette price where specific equals ad valorem [2026/27 rates]"""
    # Breakeven: specific = ad_valorem
    # R22.81 = price × 30%
    # price = R22.81 / 0.30 = ~R76.03

    profile_below = ConsumptionProfile(
        cigarette_packs_20_month=10,
        cigarette_avg_price_per_pack=76.0  # Below breakeven
    )
    result_below = calculator.calculate(profile_below)
    specific_result = 10 * 22.81 * 12

    profile_above = ConsumptionProfile(
        cigarette_packs_20_month=10,
        cigarette_avg_price_per_pack=77.0  # Above breakeven
    )
    result_above = calculator.calculate(profile_above)
    ad_valorem_result = 10 * 77.0 * 0.30 * 12

    # Below breakeven should use specific rate
    assert result_below["Cigarette Excise"] == pytest.approx(specific_result, rel=0.01)
    # Above breakeven should use ad valorem rate
    assert result_above["Cigarette Excise"] == pytest.approx(ad_valorem_result, rel=0.01)
