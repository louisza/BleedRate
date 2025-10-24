"""Test tax calculation engine"""
import pytest
from pathlib import Path
from app.domain.rates import TaxRates
from app.domain.profiles import (
    PersonalProfile,
    ConsumptionProfile,
    TransportAndPropertyProfile,
    InvestmentProfile
)
from app.domain.engine import TaxEngine


@pytest.fixture
def rates():
    """Load tax rates"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    return TaxRates.load_from_yaml(rates_path)


@pytest.fixture
def engine(rates):
    """Create tax engine"""
    return TaxEngine(rates)


def test_engine_simple_salary_only(engine):
    """Test engine with only salary"""
    personal = PersonalProfile(
        annual_salary=240000,
        age=35
    )
    consumption = ConsumptionProfile()
    transport_property = TransportAndPropertyProfile()
    investment = InvestmentProfile()
    
    breakdown, total = engine.run(personal, consumption, transport_property, investment)
    
    # Should have PAYE and UIF
    breakdown_keys = list(breakdown.keys())
    has_paye = any("PAYE" in key for key in breakdown_keys)
    has_uif = any("UIF" in key for key in breakdown_keys)
    assert has_paye or has_uif
    assert total > 0


def test_engine_with_consumption(engine):
    """Test engine with consumption taxes"""
    personal = PersonalProfile(annual_salary=240000, age=35)
    consumption = ConsumptionProfile(
        std_vat_spend_month=10000,  # R10k/month spending
        litres_petrol_month=100  # 100L petrol/month
    )
    transport_property = TransportAndPropertyProfile()
    investment = InvestmentProfile()
    
    breakdown, total = engine.run(personal, consumption, transport_property, investment)
    
    # Should have some taxes
    breakdown_keys = list(breakdown.keys())
    assert len(breakdown_keys) > 0
    assert total > 0


def test_engine_with_all_profiles(engine):
    """Test engine with all profile types"""
    personal = PersonalProfile(
        annual_salary=500000,
        annual_bonus=50000,
        age=40,
        medical_members=2
    )
    
    consumption = ConsumptionProfile(
        std_vat_spend_month=15000,
        litres_petrol_month=150,
        electricity_kwh_month=800,
        beer_litres_month=20,
        beer_avg_abv=5.0,
        wine_litres_month=6,
        wine_avg_abv=12.5,
        cigarette_packs_20_month=10,
        cigarette_avg_price_per_pack=35.0,
        plastic_bags_per_month=20
    )
    
    transport_property = TransportAndPropertyProfile(
        vehicle_licence_fees_annual=500,
        tolls_annual=1200,
        municipal_rates_services_annual=12000,
        buying_property_price=2000000
    )
    
    investment = InvestmentProfile(
        sa_dividends_annual=20000,
        taxable_cgt_base_annual=50000
    )
    
    breakdown, total = engine.run(personal, consumption, transport_property, investment)
    
    # Should have multiple tax items
    assert len(breakdown) > 5
    
    # Total should be sum of all items
    category_sum = sum(breakdown.values())
    assert total == pytest.approx(category_sum, rel=0.01)


def test_engine_effective_rate(engine):
    """Test effective tax rate calculation"""
    personal = PersonalProfile(
        annual_salary=240000,
        age=35
    )
    consumption = ConsumptionProfile()
    transport_property = TransportAndPropertyProfile()
    investment = InvestmentProfile()
    
    breakdown, total = engine.run(personal, consumption, transport_property, investment)
    
    # Effective rate should be reasonable
    effective_rate = (total / 240000) * 100
    assert 0 < effective_rate < 45  # Should be between 0% and max marginal rate


def test_engine_medical_credits(engine):
    """Test medical aid tax credits reduce PAYE"""
    # Without medical aid
    personal_no_med = PersonalProfile(
        annual_salary=240000,
        age=35
    )
    _, total_no_med = engine.run(
        personal_no_med,
        ConsumptionProfile(),
        TransportAndPropertyProfile(),
        InvestmentProfile()
    )
    
    # With medical aid
    personal_with_med = PersonalProfile(
        annual_salary=240000,
        age=35,
        medical_members=2
    )
    _, total_with_med = engine.run(
        personal_with_med,
        ConsumptionProfile(),
        TransportAndPropertyProfile(),
        InvestmentProfile()
    )
    
    # Total tax should be lower with medical credits
    assert total_with_med < total_no_med


def test_engine_summary_list(engine):
    """Test summary list export format"""
    personal = PersonalProfile(annual_salary=240000, age=35)
    consumption = ConsumptionProfile(std_vat_spend_month=10000)
    transport_property = TransportAndPropertyProfile()
    investment = InvestmentProfile()
    
    breakdown, total = engine.run(personal, consumption, transport_property, investment)
    summary = engine.summary_list(personal, consumption, transport_property, investment)
    
    # Should be list of dicts
    assert isinstance(summary, list)
    assert len(summary) > 0
    
    # Each item should have required fields
    for item in summary:
        assert "category" in item
        assert "annual" in item
        assert "monthly" in item


def test_engine_zero_income(engine):
    """Test engine with zero income"""
    personal = PersonalProfile(annual_salary=0, age=25)
    
    breakdown, total = engine.run(
        personal,
        ConsumptionProfile(),
        TransportAndPropertyProfile(),
        InvestmentProfile()
    )
    
    # Should have minimal or zero total
    assert total >= 0


def test_engine_age_rebates(engine):
    """Test age-based rebates"""
    # Young person (only primary rebate)
    personal_young = PersonalProfile(annual_salary=240000, age=35)
    _, total_young = engine.run(
        personal_young,
        ConsumptionProfile(),
        TransportAndPropertyProfile(),
        InvestmentProfile()
    )
    
    # Senior (primary + secondary rebate)
    personal_senior = PersonalProfile(annual_salary=240000, age=65)
    _, total_senior = engine.run(
        personal_senior,
        ConsumptionProfile(),
        TransportAndPropertyProfile(),
        InvestmentProfile()
    )
    
    # Senior should pay less tax due to additional rebate
    assert total_senior < total_young
