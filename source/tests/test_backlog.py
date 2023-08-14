import http.client
from unittest.mock import Mock
import pytest
from backlog import BacklogTicketManager

@pytest.fixture
def mock_http_client(monkeypatch):
    mock_conn = Mock()
    monkeypatch.setattr(http.client, 'HTTPSConnection', lambda host: mock_conn)
    return mock_conn

def test_create_ticket(mock_http_client):
    manager = BacklogTicketManager(api_key='api_key', project_id='project_id')

    mock_response = Mock()
    mock_response.read.return_value.decode.return_value = '{"id": 123}'
    mock_response.status = 201
    mock_http_client.getresponse.return_value = mock_response

    response = manager.create_ticket({'summary': 'Test Issue'})
    print(response)
    print(response.status)

    assert response.status == 201

def test_update_ticket_status(mock_http_client):
    manager = BacklogTicketManager(api_key='api_key', project_id='project_id')

    mock_response = Mock()
    mock_response.status = 200
    mock_http_client.getresponse.return_value = mock_response

    response = manager.update_ticket_status(ticket_id=123, status_id=2)
    print(response)

    assert response.status == 200

def test_add_comment_to_ticket(mock_http_client):
    manager = BacklogTicketManager(api_key='api_key', project_id='project_id')

    mock_response = Mock()
    mock_response.status = 201
    mock_http_client.getresponse.return_value = mock_response

    response = manager.add_comment_to_ticket(ticket_id=123, content='Test comment')
    print(response)

    assert response.status == 201

def test_search_tickets_by_title(mock_http_client):
    manager = BacklogTicketManager(api_key='api_key', project_id='project_id')

    mock_response = Mock()
    mock_response.read.return_value.decode.return_value = '[{"id": 123, "summary": "Test Issue"}]'
    mock_response.status = 200
    mock_http_client.getresponse.return_value = mock_response

    response = manager.search_tickets_by_title(filter={'summary': 'Test Issue'})
    print(response)

    assert response == '[{"id": 123, "summary": "Test Issue"}]'
