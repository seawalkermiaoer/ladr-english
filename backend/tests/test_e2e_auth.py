import os
import pytest
import requests

# Base URL for the running server
BASE_URL = "http://localhost:8000"


def test_missing_authorization_header():
    """Test that a request without Authorization header returns 401"""
    r = requests.get(f"{BASE_URL}/api/verify")
    assert r.status_code == 401
    response_data = r.json()
    assert "Authorization" in response_data["detail"] or response_data["detail"] == "missing Authorization header"


def test_bearer_token_ok_without_secret():
    """Test that a bearer token is accepted when no secret is configured"""
    # Ensure no secret is set by clearing the environment
    # Note: This test assumes you've started the server without WORD_TOKEN_SECRET set
    r = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Bearer abc123"})
    assert r.status_code == 200
    response_data = r.json()
    assert response_data["ok"] is True
    assert response_data["token"] == "abc123"


def test_bearer_token_must_match_secret():
    """Test that when a secret is configured, only that exact token is accepted"""
    # This test assumes you've started the server with WORD_TOKEN_SECRET=secret-token
    # Test with wrong token
    r = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Bearer wrong"})
    assert r.status_code == 401
    
    # Test with correct token
    r2 = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Bearer secret-token"})
    assert r2.status_code == 200
    response_data = r2.json()
    assert response_data["token"] == "secret-token"


def test_invalid_authorization_scheme():
    """Test that non-Bearer authorization schemes are rejected"""
    r = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Basic xyz"})
    assert r.status_code == 401
    response_data = r.json()
    assert response_data["detail"] == "invalid Authorization scheme"


def test_empty_or_missing_token():
    """Test that malformed bearer tokens are rejected"""
    # When there's no token part after "Bearer", it's treated as invalid scheme
    r = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Bearer"})
    assert r.status_code == 401
    response_data = r.json()
    assert response_data["detail"] == "invalid Authorization scheme"
    
    # When there's a space after "Bearer" but no token, it's also treated as invalid scheme
    r2 = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Bearer "})
    assert r2.status_code == 401
    response_data2 = r2.json()
    assert response_data2["detail"] == "invalid Authorization scheme"


def test_valid_simple_token():
    """Test that simple tokens without spaces work correctly"""
    # This test assumes you've started the server with WORD_TOKEN_SECRET=simple-token
    r = requests.get(f"{BASE_URL}/api/verify", headers={"Authorization": "Bearer simple-token"})
    assert r.status_code == 200
    response_data = r.json()
    print(response_data)
    assert response_data["token"] == "simple-token"


test_valid_simple_token()
