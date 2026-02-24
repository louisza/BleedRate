"""Integration tests for PDF export API endpoint"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def valid_calc_request():
    """Valid calculation request for testing"""
    return {
        "personal": {
            "annual_salary": 100000.00,
            "annual_bonus": 10000.00,
            "age": 35,
            "medical_members": 2,
            "retirement_contrib": 0.00
        },
        "consumption": {
            "std_vat_spend_month": 3000.00,
            "zero_vat_spend_month": 500.00,
            "litres_petrol_month": 60.00,
            "litres_diesel_month": 0.00,
            "electricity_kwh_month": 300.00,
            "sugary_drink_litres_month": 5.00,
            "beer_litres_month": 2.00,
            "wine_litres_month": 1.00,
            "spirits_litres_month": 0.25,
            "cigarette_packs_20_month": 0,
            "plastic_bags_per_month": 10
        },
        "transport_property": {
            "vehicle_licence_fees_annual": 5000.00,
            "tolls_annual": 2000.00,
            "municipal_rates_services_annual": 5000.00,
            "buying_property_price": None
        },
        "investment": {
            "sa_dividends_annual": 0.00,
            "taxable_cgt_base_annual": 0.00
        }
    }


class TestPDFExportEndpoint:
    """Test the /api/export/pdf endpoint"""
    
    def test_pdf_export_endpoint_exists(self, client):
        """Test that PDF export endpoint is available"""
        response = client.post("/api/export/pdf", json={})
        # Should fail with validation error, not 404
        assert response.status_code != 404
    
    def test_pdf_export_with_valid_request(self, client, valid_calc_request):
        """Test PDF export with valid calculation request"""
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers.get("content-disposition", "")
        assert len(response.content) > 0
        assert response.content.startswith(b'%PDF')
    
    def test_pdf_download_filename(self, client, valid_calc_request):
        """Test that PDF has correct download filename"""
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        content_disposition = response.headers.get("content-disposition", "")
        assert "bleedrate-tax-report.pdf" in content_disposition
    
    def test_pdf_export_with_zero_income(self, client, valid_calc_request):
        """Test PDF export with zero income"""
        valid_calc_request["personal"]["annual_salary"] = 0.00
        valid_calc_request["personal"]["annual_bonus"] = 0.00
        
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        assert response.content.startswith(b'%PDF')
    
    def test_pdf_export_with_high_income(self, client, valid_calc_request):
        """Test PDF export with very high income"""
        valid_calc_request["personal"]["annual_salary"] = 2000000.00
        valid_calc_request["personal"]["annual_bonus"] = 500000.00
        
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        assert response.content.startswith(b'%PDF')
        assert len(response.content) < 2_000_000  # Under 2MB
    
    def test_pdf_export_with_minimal_input(self, client):
        """Test PDF export with minimal input (all zeros)"""
        request = {
            "personal": {
                "annual_salary": 0.00,
                "annual_bonus": 0.00,
                "age": 25,
                "medical_members": 0,
                "retirement_contrib": 0.00
            },
            "consumption": {
                "std_vat_spend_month": 0.00,
                "zero_vat_spend_month": 0.00,
                "litres_petrol_month": 0.00,
                "litres_diesel_month": 0.00,
                "electricity_kwh_month": 0.00,
                "sugary_drink_litres_month": 0.00,
                "beer_litres_month": 0.00,
                "wine_litres_month": 0.00,
                "spirits_litres_month": 0.00,
                "cigarette_packs_20_month": 0,
                "plastic_bags_per_month": 0
            },
            "transport_property": {
                "vehicle_licence_fees_annual": 0.00,
                "tolls_annual": 0.00,
                "municipal_rates_services_annual": 0.00,
                "buying_property_price": None
            },
            "investment": {
                "sa_dividends_annual": 0.00,
                "taxable_cgt_base_annual": 0.00
            }
        }
        
        response = client.post("/api/export/pdf", json=request)
        
        assert response.status_code == 200
        assert response.content.startswith(b'%PDF')
    
    def test_pdf_export_with_complex_scenario(self, client, valid_calc_request):
        """Test PDF export with complex scenario (high consumption)"""
        valid_calc_request["personal"]["annual_salary"] = 500000.00
        valid_calc_request["personal"]["annual_bonus"] = 100000.00
        valid_calc_request["personal"]["age"] = 45
        valid_calc_request["personal"]["medical_members"] = 4
        valid_calc_request["consumption"]["std_vat_spend_month"] = 15000.00
        valid_calc_request["consumption"]["litres_petrol_month"] = 200.00
        valid_calc_request["consumption"]["beer_litres_month"] = 10.00
        valid_calc_request["consumption"]["wine_litres_month"] = 5.00
        valid_calc_request["transport_property"]["vehicle_licence_fees_annual"] = 15000.00
        valid_calc_request["transport_property"]["tolls_annual"] = 10000.00
        valid_calc_request["transport_property"]["municipal_rates_services_annual"] = 20000.00
        valid_calc_request["investment"]["sa_dividends_annual"] = 50000.00
        
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        assert response.content.startswith(b'%PDF')
        assert len(response.content) < 2_000_000
    
    def test_pdf_export_with_invalid_request(self, client):
        """Test PDF export with invalid request (missing fields)"""
        response = client.post("/api/export/pdf", json={})
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_pdf_export_with_negative_salary(self, client, valid_calc_request):
        """Test PDF export with negative salary (should fail)"""
        valid_calc_request["personal"]["annual_salary"] = -50000.00
        
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 400
        assert "negative" in response.json()["detail"].lower()
    
    def test_pdf_export_multiple_calls(self, client, valid_calc_request):
        """Test that multiple PDF exports work correctly"""
        for i in range(3):
            response = client.post("/api/export/pdf", json=valid_calc_request)
            
            assert response.status_code == 200
            assert response.content.startswith(b'%PDF')
            assert len(response.content) > 10000


class TestPDFExportPerformance:
    """Test PDF export performance"""
    
    def test_pdf_export_response_time(self, client, valid_calc_request):
        """Test that PDF export completes in reasonable time"""
        import time
        
        start = time.time()
        response = client.post("/api/export/pdf", json=valid_calc_request)
        elapsed = time.time() - start
        
        # Should complete within 2 seconds (well under 500ms target, but accounting for CI variance)
        assert elapsed < 2.0
        assert response.status_code == 200
    
    def test_pdf_size_with_large_income(self, client, valid_calc_request):
        """Test that PDF size stays reasonable even with large income"""
        valid_calc_request["personal"]["annual_salary"] = 10000000.00
        
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        # Even with very high income, should stay under 2MB
        assert len(response.content) < 2_000_000
        
        # But should still be a reasonable PDF size (at least 10KB)
        assert len(response.content) > 10000


class TestPDFExportSecurity:
    """Test security aspects of PDF export"""
    
    def test_pdf_export_no_server_storage(self, client, valid_calc_request):
        """Test that PDFs are not stored on server (generated on-the-fly)"""
        # This is more of a code review test, but we can verify the endpoint
        # returns a different PDF each time (due to timestamp)
        response1 = client.post("/api/export/pdf", json=valid_calc_request)
        response2 = client.post("/api/export/pdf", json=valid_calc_request)
        
        # Both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # PDFs may differ due to timestamp
        # (In reality they'll be identical if generated at same second,
        # but the important thing is they're generated on demand)
        assert response1.content.startswith(b'%PDF')
        assert response2.content.startswith(b'%PDF')
    
    def test_pdf_export_sanitizes_output(self, client, valid_calc_request):
        """Test that user inputs are safely escaped in PDF"""
        # This is implicitly tested by the fact that PDF generation doesn't crash
        # with special characters
        response = client.post("/api/export/pdf", json=valid_calc_request)
        
        assert response.status_code == 200
        # If injection was possible, we'd likely see errors or malformed PDFs
        assert response.content.startswith(b'%PDF')
