from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .twitter_client import TwitterClient
import json

@ensure_csrf_cookie
def index(request):
    """
    Renders the main dashboard page.
    Injects CSRF cookie and passes initial developer mock configurations from the session.
    """
    # Fetch configurations, defaults are latency=0.6s, status_code="200" OK
    dev_latency = request.session.get('dev_latency', 0.6)
    dev_status = request.session.get('dev_status', '200')
    
    context = {
        'dev_latency': dev_latency,
        'dev_status': dev_status,
    }
    return render(request, 'tweets/index.html', context)

@require_GET
def fetch_tweets_api(request):
    """
    AJAX endpoint to retrieve a user's details and their latest 5 tweets.
    Runs in developer mock mode with configurable latency and status simulations.
    """
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)
    
    # Retrieve configuration from session
    dev_latency = float(request.session.get('dev_latency', 0.6))
    dev_status = request.session.get('dev_status', '200')
    
    try:
        client = TwitterClient(latency=dev_latency, simulate_status=dev_status)
        data = client.fetch_user_and_tweets(username)
        return JsonResponse(data)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': f"API Error: {str(e)}"}, status=500)

@require_POST
def update_credentials_api(request):
    """
    AJAX endpoint to update developer settings (latency, simulated error status) in session.
    Repurposed from update_credentials for developer control board.
    """
    try:
        body = json.loads(request.body)
        latency = body.get('latency', 0.6)
        status_code = body.get('status_code', '200')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        
    try:
        request.session['dev_latency'] = float(latency)
    except ValueError:
        return JsonResponse({'error': 'Invalid latency value'}, status=400)
        
    request.session['dev_status'] = str(status_code)
    
    return JsonResponse({
        'status': 'success',
        'dev_latency': request.session['dev_latency'],
        'dev_status': request.session['dev_status'],
        'message': 'Developer Mock configurations saved.'
    })
