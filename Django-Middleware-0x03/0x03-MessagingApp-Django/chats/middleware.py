import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', level=logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Chat is only accessible from 6AM to 9PM.")
        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_timestamps = {}

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get('REMOTE_ADDR')
            now = datetime.now()

            self.ip_timestamps.setdefault(ip, [])
            self.ip_timestamps[ip] = [
                t for t in self.ip_timestamps[ip] if now - t < timedelta(minutes=1)
            ]
            if len(self.ip_timestamps[ip]) >= 5:
                return JsonResponse({"error": "Rate limit exceeded"}, status=429)

            self.ip_timestamps[ip].append(now)

        return self.get_response(request)

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/chats/protected/']  # Customize this path
        if request.path in protected_paths:
            user = request.user
            if not user.is_authenticated or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied.")
        return self.get_response(request)