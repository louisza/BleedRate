"""Test vehicle import duty calculations"""
import pytest
from pathlib import Path
from app.domain.rates import TaxRates
from app.domain.profiles import TransportAndPropertyProfile
from app.domain.calculators import PropertyTransportCalculator


@pytest.fixture
def rates():
    """Load tax rates"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    return TaxRates.load_from_yaml(rates_path)


@pytest.fixture
def calculator(rates):
    """Create property/transport calculator"""
    return PropertyTransportCalculator(rates)


def test_imported_vehicle_duty_calculation(calculator):
    """Test import duty calculation for imported vehicle"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=10000.0,  # R10k/month
        vehicle_is_imported=True  # NOT assembled in SA
    )
    
    result = calculator.calculate(profile)
    
    # Should have import duty entry
    assert "Vehicle Import Duty (in installments)" in result
    
    # Annual installments: R10k × 12 = R120k
    # Import duty is 25% of base price
    # Duty portion = 25/125 of total price = 20% of installment
    # R120k × 20% = R24,000
    expected_duty = 10000 * 12 * (25 / 125)
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(expected_duty, rel=0.01)
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(24000.0, rel=0.01)


def test_locally_assembled_vehicle_no_duty(calculator):
    """Test that locally assembled vehicles have no import duty"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=10000.0,
        vehicle_is_imported=False  # Assembled in SA (e.g., VW Polo, BMW X3)
    )
    
    result = calculator.calculate(profile)
    
    # Should NOT have import duty entry
    assert "Vehicle Import Duty (in installments)" not in result


def test_no_vehicle_financing(calculator):
    """Test with no vehicle financing"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=0.0,
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # No import duty if no installment
    assert "Vehicle Import Duty (in installments)" not in result


def test_realistic_imported_luxury_vehicle(calculator):
    """Test with realistic luxury imported vehicle"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=15000.0,  # R15k/month (e.g., Audi Q5)
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # R15k × 12 = R180k annual
    # 20% = R36,000 in import duty
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(36000.0, rel=0.01)


def test_affordable_imported_vehicle(calculator):
    """Test with affordable imported vehicle"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=5000.0,  # R5k/month (e.g., Hyundai i20)
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # R5k × 12 = R60k annual
    # 20% = R12,000 in import duty
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(12000.0, rel=0.01)


def test_combined_transport_costs_with_import(calculator):
    """Test all transport costs combined with imported vehicle"""
    profile = TransportAndPropertyProfile(
        vehicle_licence_fees_annual=1500.0,
        tolls_annual=3000.0,
        municipal_rates_services_annual=12000.0,
        vehicle_monthly_installment=8000.0,
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # Check all entries present
    assert "Vehicle License Fees" in result
    assert "Toll Fees" in result
    assert "Municipal Rates & Services" in result
    assert "Vehicle Import Duty (in installments)" in result
    
    # Verify import duty calculation
    expected_duty = 8000 * 12 * 0.20
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(expected_duty, rel=0.01)


def test_combined_transport_costs_with_local_vehicle(calculator):
    """Test all transport costs with locally assembled vehicle"""
    profile = TransportAndPropertyProfile(
        vehicle_licence_fees_annual=1500.0,
        tolls_annual=3000.0,
        municipal_rates_services_annual=12000.0,
        vehicle_monthly_installment=8000.0,
        vehicle_is_imported=False  # VW Polo, Toyota Corolla Cross, etc.
    )
    
    result = calculator.calculate(profile)
    
    # Check transport entries present
    assert "Vehicle License Fees" in result
    assert "Toll Fees" in result
    assert "Municipal Rates & Services" in result
    
    # NO import duty for locally assembled
    assert "Vehicle Import Duty (in installments)" not in result


def test_import_duty_percentage_calculation():
    """Test the 25/125 calculation logic"""
    # If base price is R100k and import duty is 25%:
    # Total price = R100k + R25k = R125k
    # Duty as % of total = R25k / R125k = 20%
    
    base_price = 100000
    import_duty_rate = 0.25
    duty_amount = base_price * import_duty_rate  # R25k
    total_price = base_price + duty_amount  # R125k
    duty_percentage_of_total = duty_amount / total_price
    
    assert duty_percentage_of_total == pytest.approx(0.20, rel=0.001)
    assert duty_percentage_of_total == pytest.approx(25/125, rel=0.001)


def test_high_end_imported_vehicle(calculator):
    """Test with high-end imported vehicle (e.g., Porsche)"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=30000.0,  # R30k/month
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # R30k × 12 = R360k annual
    # 20% = R72,000 in import duty per year!
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(72000.0, rel=0.01)


def test_locally_assembled_examples(calculator):
    """Document locally assembled vehicles with no duty"""
    # These vehicles should have vehicle_is_imported=False:
    locally_assembled = [
        "VW Polo (all generations since 1996)",
        "VW Polo Vivo (since 2010)",
        "Toyota Corolla Cross (since 2021)",
        "Toyota Fortuner (since 2015)",
        "Mercedes-Benz C-Class W206 (current gen)",
        "BMW X3 G45 (4th gen, 2025→)",
    ]
    
    # Simulate multiple local vehicles
    for _ in locally_assembled:
        profile = TransportAndPropertyProfile(
            vehicle_monthly_installment=12000.0,
            vehicle_is_imported=False
        )
        result = calculator.calculate(profile)
        
        # None should have import duty
        assert "Vehicle Import Duty (in installments)" not in result


def test_edge_case_zero_installment_imported(calculator):
    """Test edge case: imported vehicle marked but no installment"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=0.0,
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # Should not calculate duty if no installment
    assert "Vehicle Import Duty (in installments)" not in result


def test_small_installment_imported(calculator):
    """Test with very small installment (e.g., paid off vehicle)"""
    profile = TransportAndPropertyProfile(
        vehicle_monthly_installment=500.0,  # Final payments
        vehicle_is_imported=True
    )
    
    result = calculator.calculate(profile)
    
    # Should still calculate duty proportion
    expected_duty = 500 * 12 * 0.20  # R1,200/year
    assert result["Vehicle Import Duty (in installments)"] == pytest.approx(1200.0, rel=0.01)
