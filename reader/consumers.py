import json
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
import os
from itertools import islice

class FileReaderConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def read_file_chunk(self, file_path, page_number, lines_per_page=100):
        start_line = (page_number - 1) * lines_per_page
        
        with open(file_path, 'r') as file:
            # Skip to start_line efficiently and read lines_per_page lines
            return [line.strip() for line in islice(file, start_line, start_line + lines_per_page)]

    def get_total_lines(self, file_path):
        # Use a buffer to count lines efficiently
        with open(file_path, 'rb') as f:
            lines = sum(1 for _ in f)
        return lines

    def receive(self, text_data):
        data = json.loads(text_data)
        page = int(data.get('page', 1))
        file_id = data.get('file_id')
        lines_per_page = int(data.get('lines_per_page', 100))
        
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, file_id)
            lines = self.read_file_chunk(file_path, page, lines_per_page)
            total_lines = self.get_total_lines(file_path)
            total_pages = (total_lines + lines_per_page - 1) // lines_per_page
            
            self.send(text_data=json.dumps({
                'lines': lines,
                'page': page,
                'total_pages': total_pages,
                'status': 'success'
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'error': str(e),
                'status': 'error'
            }))