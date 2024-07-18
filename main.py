from extractFileData import ExtractFileData
from dotenv import load_dotenv
import os

load_dotenv()

if __name__=="__main__":

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    bucket_key = os.getenv('BUCKET_KEY')
    file_name = 'parking1949.dwg'
    
    # Read the file as binary
    with open(file_name, 'rb') as file:
        file_buffer = file.read()
        
    extractor = ExtractFileData(client_id, client_secret)
    token = extractor.get_auth_token()
    if token:
        extractor.upload_file(bucket_key, file_name, file_buffer)
        guid = extractor.get_metadata()
        if guid:
            properties = extractor.get_properties(guid)
            print(properties)
        