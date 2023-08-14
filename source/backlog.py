import http.client
from urllib.parse import urlencode

class BacklogTicketManager:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = f'{project_id}.backlog.com'

    def send_request(self, method, path, payload=None, params=None):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        if params is None:
            params = {}
        params['apiKey'] = self.api_key

        conn = http.client.HTTPSConnection(self.base_url)
        conn.request(method, path + '?' + urlencode(params), headers=headers, body=urlencode(payload))

        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        return response, data

    def create_ticket(self, _payload):
        path = '/api/v2/issues'
        payload = {
            'projectId': self.project_id,
            'issueTypeId': 1,
            **_payload
        }

        response, _ = self.send_request('POST', path, payload)
        return response

    def update_ticket_status(self, ticket_id, status_id):
        path = f'/api/v2/issues/{ticket_id}'
        payload = {
            'statusId': status_id,
        }

        response, _ = self.send_request('PATCH', path, payload)
        return response

    def add_comment_to_ticket(self, ticket_id, content):
        path = f'/api/v2/issues/{ticket_id}/comments'
        payload = {
            'content': content,
        }

        response, _ = self.send_request('POST', path, payload)
        return response

    def search_tickets_by_title(self, filter):
        path = '/api/v2/issues'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'apiKey': self.api_key,
            'projectId[]': self.project_id,
            **filter
        }

        conn = http.client.HTTPSConnection(self.base_url)
        conn.request('GET', path + '?' + urlencode(params), headers=headers)

        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        return data
