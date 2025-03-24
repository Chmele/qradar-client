import pytest
from unittest.mock import Mock
from oneliner import QRadar

@pytest.fixture
def mock_transport():
    transport = Mock()
    transport.headers = {}
    transport.verify = True
    return transport

@pytest.fixture
def qradar_instance(mock_transport):
    endpoints_response = [
        {"http_method": "GET", "path": "/users"},
        {"http_method": "POST", "path": "/offenses"},
    ]
    mock_transport.request.return_value.json.return_value = endpoints_response
    qradar = QRadar("https://qradar.example.com", "test_key", "12.0", mock_transport)
    return qradar

def test_dynamic_methods_creation(qradar_instance):
    assert hasattr(qradar_instance, "get_users")
    assert hasattr(qradar_instance, "post_offenses")

def test_dynamic_method_calls(qradar_instance, mock_transport):
    def request_side_effect(method, url, headers=None, params=None, json=None):
        if method == "GET" and url == "https://qradar.example.com/api/users":
            return Mock(json=lambda: {"users": ["user1", "user2"]})
        elif method == "POST" and url == "https://qradar.example.com/api/offenses":
            return Mock(json=lambda: {"status": "created"})
        else:
            return Mock(json=lambda: {"error": "unknown endpoint"})

    mock_transport.request.side_effect = request_side_effect

    users = qradar_instance.get_users()
    offenses = qradar_instance.post_offenses(json={"offense": "test"})

    assert users == {"users": ["user1", "user2"]}
    assert offenses == {"status": "created"}

    mock_transport.request.assert_any_call(
        'GET', 'https://qradar.example.com/api/users', params={}, json=None, headers={'Accept': 'application/json', 'Version': '12.0', 'SEC': 'test_key'})
    mock_transport.request.assert_any_call(
        'POST', 'https://qradar.example.com/api/offenses', params={'json': {'offense': 'test'}}, json=None, headers={'Accept': 'application/json', 'Version': '12.0', 'SEC': 'test_key'})

def test_dynamic_method_with_params(qradar_instance, mock_transport):
    def request_side_effect(method, url, headers=None, params=None, json=None):
        if method == "GET" and url == "https://qradar.example.com/api/users":
            return Mock(json=lambda: {"users": ["user1", "user2"]})
        elif method == "POST" and url == "https://qradar.example.com/api/offenses":
            return Mock(json=lambda: {"status": "created"})
        else:
            return Mock(json=lambda: {"error": "unknown endpoint"})

    mock_transport.request.side_effect = request_side_effect

    users = qradar_instance.get_users(filter="active", limit=10)

    assert users == {"users": ["user1", "user2"]}
    print(mock_transport.request.mock_calls)
    mock_transport.request.assert_called_with(
        "GET",
        "https://qradar.example.com/api/users",
        params={"filter": "active", "limit": 10},
        headers={'Accept': 'application/json', 'Version': '12.0', 'SEC': 'test_key'},
        json=None,
    )
