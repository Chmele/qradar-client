import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from qradar.async_client import QRadar

@pytest.fixture
def mock_transport():
    transport = Mock()
    transport.headers = {}
    transport.verify = True
    return transport

@pytest.fixture
def qradar_client(mock_transport):
    return QRadar(
        url="https://qradar.example.com",
        key="test-key",
        version="14.0",
        transport=mock_transport,
    )

def test_constructor_initialization(qradar_client):
    assert qradar_client.url == "https://qradar.example.com/api"
    assert qradar_client.version == "14.0"
    assert qradar_client.session.headers == {
        "Accept": "application/json",
        "Version": "14.0",
        "SEC": "test-key",
    }
    assert qradar_client.session.verify is True

class AwaitableMock(AsyncMock):
    def __await__(self):
        self.await_count += 1
        return iter([])

@pytest.mark.asyncio
async def test_set_methods(qradar_client, mock_transport):
    def request_side_effect(method, url, headers=None, params=None, json=None):
        if method == "GET" and url == "https://qradar.example.com/api/help/endpoints":
            return AsyncMock(json=lambda:[
                {"http_method": "GET", "path": "/test/path1"},
                {"http_method": "POST", "path": "/test/path2/{id}"}
            ])
        elif method == "GET" and url == "https://qradar.example.com/api/test/path1":
            return AsyncMock(json=lambda:[{}])
        else:
            AsyncMock(json=lambda:{"unknown"})
    mock_transport.request = AsyncMock()
    mock_transport.request.side_effect = request_side_effect
    
    await qradar_client.set_methods()
    mock_transport.request.assert_awaited_with('GET', 'https://qradar.example.com/api/help/endpoints', params={'filter': 'version=14.0'}, json=None)
    path1 = await qradar_client.get_test_path1(test="test")
    assert path1 == [{}]
    mock_transport.request.assert_awaited_with('GET', 'https://qradar.example.com/api/test/path1', params={'test': 'test'}, json=None)
