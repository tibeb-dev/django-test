import requests
import os
from django.conf import settings

def download_sample_file():
    """Downloads a sample large text file if it doesn't exist"""
    # Using Project Gutenberg's Complete Works of William Shakespeare as an example
    url = "https://examplefile.com/file-download/25"
    file_path = os.path.join(settings.MEDIA_ROOT, "sample.txt")
    
    if not os.path.exists(file_path):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers, stream=True)  # Adeded headers
            response.raise_for_status()
            
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Error downloading sample file: {e}")
            return False
    return True 