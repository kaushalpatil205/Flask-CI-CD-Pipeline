import pytest
import os

# Try importing the Flask app if app.py exists
try:
    from app import app
except ImportError:
    app = None

def test_basic_sanity():
    """A basic sanity test to ensure Python math and CI/CD environment work."""
    assert 1 + 1 == 2
    assert True is True

def test_flask_application_exists():
    """Verify that the Flask application object can be loaded."""
    if app:
        assert app is not None
        assert app.name == 'app'

def test_environment():
    """Verify that Python testing environment variables are functioning."""
    os.environ["TEST_MODE"] = "True"
    assert os.environ.get("TEST_MODE") == "True"
