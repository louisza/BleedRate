"""Tests for blog, FAQ, privacy, terms, sitemap, robots.txt routes"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_blog_list(client):
    """GET /blog returns 200 and lists posts"""
    response = client.get("/blog")
    assert response.status_code == 200
    assert "Tax Guides" in response.text or "tax" in response.text.lower()
    assert "SARS" in response.text or "South African" in response.text


def test_blog_post_how_much_tax(client):
    """GET /blog/how-much-tax-do-south-africans-really-pay returns 200"""
    response = client.get("/blog/how-much-tax-do-south-africans-really-pay")
    assert response.status_code == 200
    assert "PAYE" in response.text
    assert "Beyond PAYE" in response.text or "really pay" in response.text.lower()


def test_blog_post_tax_brackets(client):
    """GET /blog/sars-tax-brackets-2025-2026-explained returns 200"""
    response = client.get("/blog/sars-tax-brackets-2025-2026-explained")
    assert response.status_code == 200
    assert "bracket" in response.text.lower()
    assert "rebate" in response.text.lower()


def test_blog_post_fuel_levy(client):
    """GET /blog/fuel-levy-south-africa-2025 returns 200"""
    response = client.get("/blog/fuel-levy-south-africa-2025")
    assert response.status_code == 200
    assert "Fuel Levy" in response.text or "fuel levy" in response.text.lower()
    assert "R6.33" in response.text or "litre" in response.text.lower()


def test_blog_post_vat(client):
    """GET /blog/vat-south-africa-what-is-zero-rated returns 200"""
    response = client.get("/blog/vat-south-africa-what-is-zero-rated")
    assert response.status_code == 200
    assert "VAT" in response.text
    assert "zero" in response.text.lower()


def test_blog_post_provisional_tax(client):
    """GET /blog/provisional-tax-freelancers-south-africa returns 200"""
    response = client.get("/blog/provisional-tax-freelancers-south-africa")
    assert response.status_code == 200
    assert "provisional" in response.text.lower()
    assert "freelan" in response.text.lower()


def test_blog_post_not_found(client):
    """GET /blog/nonexistent-slug returns 404"""
    response = client.get("/blog/this-does-not-exist-xyz")
    assert response.status_code == 404


def test_faq_page(client):
    """GET /faq returns 200"""
    response = client.get("/faq")
    assert response.status_code == 200
    assert "faq" in response.text.lower() or "FAQ" in response.text


def test_privacy_page(client):
    """GET /privacy returns 200"""
    response = client.get("/privacy")
    assert response.status_code == 200
    assert "privacy" in response.text.lower()


def test_terms_page(client):
    """GET /terms returns 200"""
    response = client.get("/terms")
    assert response.status_code == 200
    assert "terms" in response.text.lower()


def test_sitemap_xml(client):
    """GET /sitemap.xml returns valid XML with blog URLs"""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "bleedrate.co.za" in response.text
    assert "/blog/" in response.text
    assert "urlset" in response.text


def test_robots_txt(client):
    """GET /robots.txt returns valid robots.txt"""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent" in response.text
    assert "Sitemap" in response.text
    assert "bleedrate.co.za" in response.text


def test_blog_list_contains_all_posts(client):
    """Blog list page should contain all 5 post titles"""
    response = client.get("/blog")
    assert response.status_code == 200
    assert "how-much-tax" in response.text or "Beyond PAYE" in response.text
    assert "Tax Brackets" in response.text or "bracket" in response.text.lower()
    assert "Fuel Levy" in response.text or "fuel" in response.text.lower()
    assert "VAT" in response.text
    assert "Provisional" in response.text or "freelan" in response.text.lower()
