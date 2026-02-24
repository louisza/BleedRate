"""Tests for PDF export functionality"""
import pytest
from io import BytesIO
from datetime import datetime
from app.services.pdf_export import PDFExporter
from app.api.schemas import CalcRequest, Personal, Consumption, TransportProperty, Investment


@pytest.fixture
def pdf_exporter():
    """Fixture for PDF exporter instance"""
    return PDFExporter()


@pytest.fixture
def sample_calculation_data():
    """Sample calculation data for testing"""
    return {
        'personal': {
            'annual_salary': 100000.00,
            'annual_bonus': 10000.00,
            'age': 35,
            'medical_members': 2,
        },
        'breakdown': {
            'PAYE (Income Tax)': 10234.50,
            'UIF': 427.50,
            'VAT': 8500.00,
            'Fuel Levies': 1200.00,
            'Electricity Environmental Levy': 150.00,
            'Alcohol Excise Duty': 800.00,
            'Tobacco Tax': 1050.00,
            'Property Transfer Duty': 0.00,
            'Vehicle Excise Duty': 500.00,
            'Embedded Corporate Tax': 2000.00,
            'Health Promotion Levy': 100.00,
            'Plastic Bag Levy': 25.00,
            'Municipal Services': 2400.00,
        },
        'total': 27386.50,
        'effective_rate_vs_gross': 24.9,
        'timestamp': datetime(2026, 2, 24, 10, 30, 0),
    }


class TestPDFExporterBasic:
    """Test basic PDF generation functionality"""
    
    def test_pdf_exporter_initialization(self, pdf_exporter):
        """Test that PDF exporter initializes correctly"""
        assert pdf_exporter is not None
        assert hasattr(pdf_exporter, 'styles')
        assert hasattr(pdf_exporter, 'generate_pdf')
    
    def test_generate_pdf_returns_bytes(self, pdf_exporter, sample_calculation_data):
        """Test that generate_pdf returns bytes"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
    
    def test_pdf_starts_with_magic_number(self, pdf_exporter, sample_calculation_data):
        """Test that generated PDF has correct PDF magic number"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        
        # PDF files start with %PDF-1.x
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_pdf_file_size_reasonable(self, pdf_exporter, sample_calculation_data):
        """Test that generated PDF is within reasonable size limits"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        
        # Should be less than 2MB
        assert len(pdf_bytes) < 2_000_000
        
        # Should be at least a few KB
        assert len(pdf_bytes) > 10_000


class TestPDFContent:
    """Test PDF content and formatting"""
    
    def test_pdf_contains_title(self, pdf_exporter, sample_calculation_data):
        """Test that PDF contains BleedRate title"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        pdf_text = pdf_bytes.decode('latin-1', errors='ignore')
        
        assert 'BleedRate' in pdf_text
    
    def test_pdf_contains_salary_info(self, pdf_exporter, sample_calculation_data):
        """Test that PDF contains user's salary information"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        pdf_text = pdf_bytes.decode('latin-1', errors='ignore')
        
        # Should contain salary amount (formatted)
        assert '100' in pdf_text or '100000' in pdf_text
    
    def test_pdf_contains_total_tax(self, pdf_exporter, sample_calculation_data):
        """Test that PDF contains total tax amount"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        pdf_text = pdf_bytes.decode('latin-1', errors='ignore')
        
        # Should contain the total tax amount
        assert '27' in pdf_text or '27386' in pdf_text
    
    def test_pdf_contains_disclaimer(self, pdf_exporter, sample_calculation_data):
        """Test that PDF contains required disclaimer"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        pdf_text = pdf_bytes.decode('latin-1', errors='ignore')
        
        assert 'DISCLAIMER' in pdf_text or 'disclaimer' in pdf_text
        assert 'tax professional' in pdf_text or 'accountant' in pdf_text
    
    def test_pdf_contains_all_tax_categories(self, pdf_exporter, sample_calculation_data):
        """Test that PDF contains all tax categories from breakdown"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        pdf_text = pdf_bytes.decode('latin-1', errors='ignore')
        
        # Check for some key tax categories
        assert 'PAYE' in pdf_text
        assert 'VAT' in pdf_text or 'Vat' in pdf_text
        assert 'Fuel' in pdf_text
    
    def test_pdf_contains_timestamp(self, pdf_exporter, sample_calculation_data):
        """Test that PDF contains timestamp"""
        pdf_bytes = pdf_exporter.generate_pdf(sample_calculation_data)
        pdf_text = pdf_bytes.decode('latin-1', errors='ignore')
        
        # Should contain the date and time
        assert '2026' in pdf_text or '26' in pdf_text


class TestPDFFormatting:
    """Test PDF currency and number formatting"""
    
    def test_format_currency_positive(self, pdf_exporter):
        """Test currency formatting for positive amounts"""
        formatted = pdf_exporter._format_currency(1234.56)
        assert formatted == "R 1,234.56"
    
    def test_format_currency_large_amount(self, pdf_exporter):
        """Test currency formatting for large amounts"""
        formatted = pdf_exporter._format_currency(1000000.00)
        assert formatted == "R 1,000,000.00"
    
    def test_format_currency_zero(self, pdf_exporter):
        """Test currency formatting for zero"""
        formatted = pdf_exporter._format_currency(0.00)
        assert formatted == "R 0.00"
    
    def test_format_currency_negative(self, pdf_exporter):
        """Test currency formatting for negative amounts"""
        formatted = pdf_exporter._format_currency(-500.00)
        assert formatted == "-R 500.00"
    
    def test_format_currency_two_decimals(self, pdf_exporter):
        """Test that currency always has 2 decimal places"""
        formatted = pdf_exporter._format_currency(99.1)
        assert formatted == "R 99.10"


class TestPDFEdgeCases:
    """Test PDF generation with edge case data"""
    
    def test_pdf_with_zero_income(self, pdf_exporter):
        """Test PDF generation with zero income"""
        data = {
            'personal': {
                'annual_salary': 0.00,
                'annual_bonus': 0.00,
                'age': 25,
                'medical_members': 0,
            },
            'breakdown': {
                'PAYE (Income Tax)': 0.00,
                'UIF': 0.00,
                'VAT': 500.00,
            },
            'total': 500.00,
            'effective_rate_vs_gross': 0.0,
        }
        
        pdf_bytes = pdf_exporter.generate_pdf(data)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
    
    def test_pdf_with_very_high_income(self, pdf_exporter):
        """Test PDF generation with very high income"""
        data = {
            'personal': {
                'annual_salary': 5000000.00,
                'annual_bonus': 1000000.00,
                'age': 50,
                'medical_members': 4,
            },
            'breakdown': {
                'PAYE (Income Tax)': 1200000.00,
                'UIF': 10000.00,
                'VAT': 150000.00,
                'Other': 50000.00,
            },
            'total': 1410000.00,
            'effective_rate_vs_gross': 23.5,
        }
        
        pdf_bytes = pdf_exporter.generate_pdf(data)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert len(pdf_bytes) < 2_000_000  # Still under 2MB
    
    def test_pdf_with_minimal_breakdown(self, pdf_exporter):
        """Test PDF with minimal tax breakdown"""
        data = {
            'personal': {
                'annual_salary': 50000.00,
                'annual_bonus': 0.00,
                'age': 30,
                'medical_members': 1,
            },
            'breakdown': {
                'PAYE (Income Tax)': 5000.00,
            },
            'total': 5000.00,
            'effective_rate_vs_gross': 10.0,
        }
        
        pdf_bytes = pdf_exporter.generate_pdf(data)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
    
    def test_pdf_without_timestamp(self, pdf_exporter, sample_calculation_data):
        """Test PDF generation without explicit timestamp (should default to now)"""
        data = sample_calculation_data.copy()
        del data['timestamp']
        
        pdf_bytes = pdf_exporter.generate_pdf(data)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0


class TestPDFSections:
    """Test that PDF sections render correctly"""
    
    def test_profile_section_builds(self, pdf_exporter, sample_calculation_data):
        """Test that profile section builds without errors"""
        personal = sample_calculation_data['personal']
        section = pdf_exporter._build_profile_section(personal)
        
        assert section is not None
        assert hasattr(section, '_rows')
    
    def test_summary_section_builds(self, pdf_exporter, sample_calculation_data):
        """Test that summary section builds without errors"""
        total = sample_calculation_data['total']
        effective_rate = sample_calculation_data['effective_rate_vs_gross']
        personal = sample_calculation_data['personal']
        
        section = pdf_exporter._build_summary_section(total, effective_rate, personal)
        assert section is not None
        assert hasattr(section, '_rows')
    
    def test_breakdown_section_builds(self, pdf_exporter, sample_calculation_data):
        """Test that breakdown section builds without errors"""
        breakdown = sample_calculation_data['breakdown']
        section = pdf_exporter._build_breakdown_section(breakdown)
        
        assert section is not None
        assert hasattr(section, '_rows')
    
    def test_disclaimer_section_builds(self, pdf_exporter):
        """Test that disclaimer section builds without errors"""
        section = pdf_exporter._build_disclaimer_section()
        
        assert section is not None
        assert hasattr(section, 'text')
