import time
from flask import Blueprint, render_template, request, jsonify
from flask_wtf.csrf import CSRFError
from extensions import limiter
from helpers.telegram import send_rate_limit_alert

errors_bp = Blueprint('errors', __name__)

def csrf_error(error):
    reason = getattr(error, 'description', 'CSRF token missing or invalid.')
    if request.path.startswith('/api/') or request.is_json:
        return jsonify({'status': 400, 'error': 'Bad Request', 'message': reason}), 400
    return render_template(['Error/400.html', 'errors/400.html'], error=error, message=reason), 400

def not_found_error(error):
    if request.path.startswith('/api/') or request.is_json:
        return jsonify({'status': 404, 'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404
    return render_template(['Error/404.html', 'errors/404.html'], error=error), 404

def ratelimit_handler(error):
    retry_after = 60
    if limiter.current_limit and getattr(limiter.current_limit, 'reset_at', None):
        retry_after = max(1, int(limiter.current_limit.reset_at - time.time()))

    desc = getattr(error, 'description', 'Too Many Requests')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # Trigger Telegram security alert asynchronously
    send_rate_limit_alert(
        ip=client_ip,
        method=request.method,
        path=request.path,
        limit_desc=desc,
        retry_after=retry_after,
        user_agent=user_agent
    )

    if request.path.startswith('/api/') or request.is_json:
        return jsonify({
            'status': 429,
            'error': 'Too Many Requests',
            'message': desc,
            'retry_after': retry_after
        }), 429
    return render_template(['Error/429.html', 'errors/429.html'], error=error, retry_after=retry_after), 429

def internal_server_error(error):
    if request.path.startswith('/api/') or request.is_json:
        return jsonify({'status': 500, 'error': 'Internal Server Error', 'message': 'An internal server error occurred.'}), 500
    return render_template(['Error/500.html', 'errors/500.html'], error=error), 500

# Attach error handlers to blueprint
errors_bp.app_errorhandler(CSRFError)(csrf_error)
errors_bp.app_errorhandler(404)(not_found_error)
errors_bp.app_errorhandler(429)(ratelimit_handler)
errors_bp.app_errorhandler(500)(internal_server_error)

def register_error_handlers(app):
    app.register_error_handler(CSRFError, csrf_error)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(429, ratelimit_handler)
    app.register_error_handler(500, internal_server_error)

init_app = register_error_handlers
init_error_handlers = register_error_handlers