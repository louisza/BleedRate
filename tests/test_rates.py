"""Test tax rates loading and validation"""
import pytest
from pathlib import Path
from app.domain.rates import TaxRates


def test_load_tax_rates():
    """Test loading tax rates from YAML"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    rates = TaxRates.load_from_yaml(rates_path)
    
    # Check PAYE brackets
    assert len(rates.paye_brackets) == 7
    assert rates.paye_brackets[0].rate == 0.18
    assert rates.paye_brackets[-1].rate == 0.45
    
    # Check rebates
    assert rates.primary_rebate > 0
    assert rates.secondary_rebate > 0
    assert rates.tertiary_rebate > 0
    
    # Check VAT
    assert rates.vat_rate == 0.15
    
    # Check alcohol rates (National Treasury 2024 framework)
    assert rates.beer_excise_per_laa > 0  # LAA-based for beer
    assert rates.wine_excise_per_litre > 0  # Volumetric for wine
    assert rates.spirits_excise_per_laa > 0  # LAA-based for spirits
    assert rates.beer_typical_abv > 0
    assert rates.spirits_typical_abv > 0
    
    # Check tobacco rates
    assert rates.cigarette_excise_per_20 > 0
    assert rates.cigarette_ad_valorem_rate > 0
    assert rates.cigar_excise_per_gram > 0
    assert rates.pipe_tobacco_excise_per_gram > 0


def test_paye_brackets_ordered():
    """Test that PAYE brackets are properly ordered"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    rates = TaxRates.load_from_yaml(rates_path)
    
    for i in range(len(rates.paye_brackets) - 1):
        current = rates.paye_brackets[i]
        next_bracket = rates.paye_brackets[i + 1]
        
        if current.up_to is not None:
            assert current.lower < current.up_to
            assert current.up_to == next_bracket.lower


def test_transfer_duty_bands():
    """Test transfer duty bands"""
    rates_path = Path(__file__).parent.parent / "data" / "tax_rates.yml"
    rates = TaxRates.load_from_yaml(rates_path)
    
    assert len(rates.transfer_duty) == 6
    assert rates.transfer_duty[0].rate == 0.0  # First band is exempt
    assert rates.transfer_duty[-1].up_to is None  # Last band is open-ended
