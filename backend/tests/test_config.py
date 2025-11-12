import os
import pytest
from app.core.config import settings


def test_config_loads_from_env():
    """Test that configuration loads from environment variables."""
    # Test Supabase settings from .env file
    assert settings.SUPABASE_URL is not None
    assert "supabase.opentrust.net" in settings.SUPABASE_URL
    assert settings.SUPABASE_ANON_KEY is not None
    assert len(settings.SUPABASE_ANON_KEY) > 50  # JWT tokens are long
    
    # Test CORS settings (should be None since not set in .env)
    assert settings.WORD_ALLOWED_ORIGINS is None


def test_config_with_token_secret():
    """Test that WORD_TOKEN_SECRET can be set."""
    # Set environment variable
    os.environ["WORD_TOKEN_SECRET"] = "test-secret"
    
    # Import settings again to get updated values
    from app.core.config import settings as updated_settings
    assert updated_settings.WORD_TOKEN_SECRET == "test-secret"
    
    # Clean up
    if "WORD_TOKEN_SECRET" in os.environ:
        del os.environ["WORD_TOKEN_SECRET"]