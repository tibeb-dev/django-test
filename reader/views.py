from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from .utils import download_sample_file

def index(request):
    # Download sample file if not exists
    if download_sample_file():
        return render(request, 'reader/index.html')
    return render(request, 'reader/index.html', {'error': 'Sample file not available'})

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Create media directory if it doesn't exist
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                
        return JsonResponse({
            'status': 'success',
            'file_id': uploaded_file.name
        })
    
    # Return sample file info for initial load or fallback
    sample_file = "sample.txt"
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, sample_file)):
        return JsonResponse({
            'status': 'success',
            'file_id': sample_file
        })
        
    return JsonResponse({'status': 'error', 'message': 'Sample file not available'}, status=400)