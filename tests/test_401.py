import pytest
from unittest.mock import Mock, AsyncMock
from qradar.client import QRadar
from qradar.async_client import QRadar as AsyncQRadar


@pytest.fixture
def mock_transport():
    transport = Mock()
    transport.headers = {}
    transport.verify = True

    # Simulate the JSON body returned by QRadar on HTTP 401
    transport.request.return_value.json.return_value = {
        "http_response": {
            "code": 401,
            "message": "You are unauthorized to access the requested resource.",
        },
        "code": 18,
        "description": "",
        "details": {},
        "message": "No SEC header present in request.",
    }

    return transport

@pytest.fixture
def mock_async_transport():
    transport = Mock()
    transport.headers = {}
    transport.verify = True

    # Simulate an HTTP 401 response
    response = Mock()
    response.json.return_value = {
        "http_response": {
            "code": 401,
            "message": "You are unauthorized to access the requested resource.",
        },
        "code": 18,
        "description": "",
        "details": {},
        "message": "No SEC header present in request.",
    }

    # The async client awaits transport.request()
    transport.request = AsyncMock(return_value=response)

    return transport


def test_dynamic_methods_creation(mock_transport):
    with pytest.raises(
        AttributeError,
        match="'str' object has no attribute 'get'",
    ):
        QRadar(
            base_url="https://qradar.example.com",
            key="test_key",
            version="12.0",
            transport=mock_transport,
            verify=True,
        )
@pytest.mark.asyncio
async def test_async_dynamic_methods_creation(mock_async_transport):
    with pytest.raises(
        AttributeError,
        match="'str' object has no attribute 'get'",
    ):
        await AsyncQRadar(
            url="https://qradar.example.com",
            key="test_key",
            version="12.0",
            transport=mock_async_transport,
            verify=True,
        )
