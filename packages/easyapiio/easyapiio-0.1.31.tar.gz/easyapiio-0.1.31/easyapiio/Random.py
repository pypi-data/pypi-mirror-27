import json
import requests

class Random:
    def __init__(self, apiKey, appId):
        self.apiKey = apiKey
        self.appId = appId

    def getVersion(self):
        return '0.1.31'

    def getAPIKey(self):
        return self.apiKey

    def getAppId(self):
        return self.appId

    # Create
    def create(self):
        headers = { 'Content-type': 'application/json', 'Authorization': ('Bearer ' + str(self.apiKey)) }
        post_fields = {
            'appId': self.appId,
            'sdkVersion': self.getVersion(),
            'sdk': 'python-sdk'
        }
        result = requests.post('https://api.easyapi.io/v1/random/create', json=post_fields, headers=headers)

        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.', 'result': result }

    # Delete
    def delete(self, randomCode):
        headers = { 'Content-type': 'application/json', 'Authorization': ('Bearer ' + str(self.apiKey)) }
        post_fields = {
            'appId': self.appId,
            'randomCode': randomCode,
            'sdkVersion': self.getVersion(),
            'sdk': 'python-sdk'
        }
        result = requests.post('https://api.easyapi.io/v1/random/delete', json=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }

    # Verify
    def verify(self, randomCode):
        headers = { 'Content-type': 'application/json', 'Authorization': ('Bearer ' + str(self.apiKey)) }
        post_fields = { 'appId': self.appId, 'randomCode': randomCode }
        result = requests.post('https://api.easyapi.io/v1/random/verify', json=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }

    # List
    def list(self):
        headers = { 'Content-type': 'application/json', 'Authorization': ('Bearer ' + str(self.apiKey)) }
        post_fields = {
            'appId': self.appId,
            'sdkVersion': self.getVersion(),
            'sdk': 'python-sdk'
        }
        result = requests.post('https://api.easyapi.io/v1/random/list', json=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }
