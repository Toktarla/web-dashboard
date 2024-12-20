from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .tcp_client import TCPClient
import json

# Initialize TCP Client
tcp_client = TCPClient()


def home(request):
    # Render home page with an empty table initially
    return render(request, 'webservice/home.html')


@csrf_exempt  # For testing purposes. In production, handle CSRF properly
def send_command(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                command = data.get('command')
            else:
                command = request.POST.get('command')
                
            if command:
                response = tcp_client.send_command(command)
                return JsonResponse({'response': response})
            else:
                return JsonResponse({'error': 'No command provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
