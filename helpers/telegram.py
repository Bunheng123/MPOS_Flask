import time
import threading
from datetime import datetime, timezone, timedelta
import requests
from config import TELEGRAM_ALERT_BOT_TOKEN, TELEGRAM_ALERT_CHAT_ID

# In-memory alert cache to prevent Telegram spam if an attacker hits hundreds of times
_recent_alerts = {}
_lock = threading.Lock()
ALERT_COOLDOWN_SECONDS = 60

def _escape_html(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _send_alert_worker(ip, method, path, limit_desc, retry_after, user_agent):
    now = time.time()
    
    with _lock:
        last_info = _recent_alerts.get(ip)
        if last_info and (now - last_info['timestamp']) < ALERT_COOLDOWN_SECONDS:
            # Increase blocked attempt count during cooldown, don't spam Telegram
            last_info['count'] += 1
            return
        # First alert or cooldown expired
        _recent_alerts[ip] = {'timestamp': now, 'count': 1}

    bot_token = TELEGRAM_ALERT_BOT_TOKEN
    chat_id = TELEGRAM_ALERT_CHAT_ID

    if not bot_token or not chat_id:
        return

    cambodia_tz = timezone(timedelta(hours=7))
    cambodia_time = datetime.now(cambodia_tz).strftime('%Y-%m-%d %I:%M:%S %p (GMT+7)')
    ua_display = _escape_html(user_agent or "Unknown")
    if len(ua_display) > 80:
        ua_display = ua_display[:77] + "..."

    message = (
    "🚨 <b>[429] RATE LIMIT TRIGGERED</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<pre><code>"
    f"Target Endpoint  : {_escape_html(method)} {_escape_html(path)}\n"
    f"Attacker IP      : {_escape_html(ip)}\n"
    f"Attempts         : {_escape_html(limit_desc)}\n"
    f"Cooldown Period  : {retry_after}s remaining\n"
    "</code></pre>"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    f"<b>Device Info:</b> <code>{ua_display}</code>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    f"⏰ <code>{cambodia_time}</code>"
)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.post(url, json=payload, headers=headers, timeout=8)
    except Exception as e:
        print(f"[Telegram Alert Error] Failed to send alert: {e}")

def send_rate_limit_alert(ip, method, path, limit_desc="Rate limit exceeded", retry_after=60, user_agent=None):
    """
    Non-blocking function to send security rate-limit alerts to Telegram.
    Runs asynchronously in a background thread so client requests are never delayed.
    """
    t = threading.Thread(
        target=_send_alert_worker,
        args=(ip, method, path, limit_desc, retry_after, user_agent),
        daemon=True
    )
    t.start()
