import requests
import base64
import time


class ExtractFileData:
    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
        self.auth_token = None
        self.urn = None
        
    def get_auth_token(self):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'bucket:read bucket:create data:read data:write'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(self.auth_url, data=data, headers=headers)
            self.auth_token = response.json().get('access_token')
            return self.auth_token
        except requests.exceptions.RequestException as e:
            print(f"error occured {e}")
            return None
            
    def upload_file(self, bucket_key, file_name, file_buffer):
        upload_url = f'https://developer.api.autodesk.com/oss/v2/buckets/{bucket_key}/objects/{file_name}'
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/octet-stream'
        }
        try:
            response = requests.put(upload_url, data=file_buffer, headers=headers)
            response.raise_for_status()
            self.urn = base64.b64encode(response.json()['objectId'].encode()).decode()
            return self.urn
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during file upload: {e}')
            return None

    def translate_file(self):
        translate_url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/job'
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'input': {'urn': self.urn},
            'output': {'formats': [{'type': 'svf', 'views': ['2d', '3d']}]}
        }
        try:
            response = requests.post(translate_url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during file translation: {e}')
            return None

    def check_translation_status(self):
        self.translate_file()
        status_url = f'https://developer.api.autodesk.com/modelderivative/v2/designdata/{self.urn}/manifest'
        headers = {
            'Authorization': f'Bearer {self.auth_token}'
        }
        while True:
            try:
                response = requests.get(status_url, headers=headers)
                response.raise_for_status()
                status = response.json().get('status')
                if status == 'failed':
                    raise Exception('Translation failed')
                if status == 'success':
                    break
                time.sleep(5)
            except requests.exceptions.RequestException as e:
                print(f'An error occurred during translation status check: {e}')
                return False
        return True

    def get_metadata(self):            
        metadata_url = f'https://developer.api.autodesk.com/modelderivative/v2/designdata/{self.urn}/metadata'
        headers = {
            'Authorization': f'Bearer {self.auth_token}'
        }
        try:
            if self.check_translation_status():
                response = requests.get(metadata_url, headers=headers)
                response.raise_for_status()
                guid = response.json()['data']['metadata'][0]['guid']
                return guid
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during metadata fetching: {e}')
            return None

    def get_properties(self, guid):
        properties_url = f'https://developer.api.autodesk.com/modelderivative/v2/designdata/{self.urn}/metadata/{guid}/properties'
        headers = {
            'Authorization': f'Bearer {self.auth_token}'
        }
        try:
            response = requests.get(properties_url, headers=headers)
            response.raise_for_status()
            properties = response.json()['data']['collection']
            return properties
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during properties fetching: {e}')
            return None
        