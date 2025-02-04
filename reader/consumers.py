import json
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
import os

class FileReaderConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def read_file_chunk(self, file_path, page_number, lines_per_page=100):
        start_line = (page_number - 1) * lines_per_page
        end_line = start_line + lines_per_page
        current_line = 0
        chunk_lines = []
        
        with open(file_path, 'r') as file:
            for line in file:
                if current_line >= start_line and current_line < end_line:
                    chunk_lines.append(line.strip())
                elif current_line >= end_line:
                    break
                current_line += 1
                
        return chunk_lines

    def receive(self, text_data):
        data = json.loads(text_data)
        page = int(data.get('page', 1))
        file_id = data.get('file_id')
        lines_per_page = int(data.get('lines_per_page', 100))
        
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, file_id)
            lines = self.read_file_chunk(file_path, page, lines_per_page)
            total_lines = sum(1 for _ in open(file_path))
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