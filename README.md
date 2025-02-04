# Real-Time Paginated File Reader

A Django application that efficiently reads large text files using WebSocket-based pagination with Django Channels and Daphne.

## Features
- Upload and read large text files (100MB+)
- Memory-efficient chunked reading (100 lines per page)
- Real-time WebSocket communication
- Simple pagination interface

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
2. bash
git clone <repository-url>
cd file_reader
2. Create and activate virtual environment:
3. bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:
4. bash
pip install -r requirements.txt

4. Run migrations:
5. bash
python manage.py migrate

## Running the Application

1. Start the Daphne server:
2. bash
daphne file_reader.asgi:application --port 8000


2. Open your browser and visit:

## Usage
1. Click "Choose File" to select a text file
2. Click "Upload" to upload the file
3. Use "Previous" and "Next" buttons to navigate through pages
4. Each page displays 100 lines of text

## Project Structure

file_reader/

├── file_reader/ # Project settings

├── reader/ # Main application

├── requirements.txt # Dependencies

└── manage.py # Django management script


## Technical Details
- Uses Django Channels for WebSocket communication
- Implements chunked file reading for memory efficiency
- Files are stored in MEDIA_ROOT directory
- Frontend communicates exclusively via WebSockets

## Troubleshooting
- If WebSocket connection fails, ensure Daphne is running
- If upload fails, check MEDIA_ROOT permissions
- For large files, ensure sufficient disk space