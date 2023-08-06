import json
from time import time

import requests

BEARER_TOKEN_URL = 'https://auth.atlassian.com/oauth/token'
SITE_API_URL = 'https://api.atlassian.com/site'
USER_API_URL = 'https://api.atlassian.com/scim/site'
MODULE_API_URL = 'https://api.atlassian.com/app/module'

class Stride:
    def __init__(self, cloud_id, client_id=None, client_secret=None, access_token=None):
        self.cloud_id = cloud_id
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = access_token
        self._access_token_expires = 0

    @property
    def access_token(self):
        if self._access_token and self._access_token_expires > time():
            return self._access_token

        # If non-bot API tokens don't have a client_id or client_secret
        if self._access_token and self.client_id is None and self.client_secret is None:
            return self._access_token

        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': 'api.atlassian.com'
        }
        r = requests.post(BEARER_TOKEN_URL, json=payload)
        r.raise_for_status()
        data = json.loads(r.text)
        self._access_token = data['access_token']
        self._access_token_expires = time() - 60 + int(data['expires_in'])
        return self._access_token

    @property
    def headers(self):
        headers = {
            'authorization': 'Bearer {}'.format(self.access_token)
        }
        return headers

    def get_room_id(self, room_name):
        params = {'query': room_name}
        r = requests.get('{}/{}/conversation'.format(SITE_API_URL, self.cloud_id),
                         params=params, headers=self.headers)
        r.raise_for_status()
        data = json.loads(r.text)
        for room in data['values']:
            if room['name'] == room_name:
                return room['id']
        return None

    def message_room(self, room_id, message_doc):
        r = requests.post('{}/{}/conversation/{}/message'.format(SITE_API_URL, self.cloud_id, room_id),
                          json=message_doc, headers=self.headers)
        r.raise_for_status()
        return r

    def message_user(self, user_id, message_doc):
        r = requests.post('{}/{}/conversation/user/{}/message'.format(SITE_API_URL, self.cloud_id, user_id),
                          json=message_doc, headers=self.headers)
        r.raise_for_status()
        return r

    def user_details(self, user_id):
        r = requests.get('{}/{}/Users/{}'.format(USER_API_URL, self.cloud_id, user_id),
                          headers=self.headers)
        r.raise_for_status()
        return r

    def glance_update(self, key, room_id, user_id, label):
        update_url = '{}/chat/conversation/chat:glance/{}/state'.format(MODULE_API_URL, key)
        update_dict = {}
        glance_context = {}
        glance_context['cloudId'] = self.cloud_id
        glance_context['conversationId'] = room_id
        glance_context['userId'] = user_id

        update_dict['context'] = glance_context
        update_dict['label'] = label

        r = requests.post(update_url, json=update_dict, headers=self.headers)
        r.raise_for_status()
        return r
