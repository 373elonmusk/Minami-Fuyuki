# ============================================================
#Group Manager Bot
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# Support: https://t.me/LearningBotsCommunity
# Channel: https://t.me/learning_bots
# YouTube: https://youtube.com/@learning_bots
# License: Open-source (keep credits, no resale)
# ============================================================

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 🔐 Import security
from security import verify_integrity, get_runtime_key

logging.basicConfig(level=logging.INFO)

verify_integrity()

RUNTIME_KEY = get_runtime_key()

# ✅ Dummy HTTP server to satisfy Render port scan
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass  # Silence HTTP logs

def run_health_server():
    import os
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

from handlers import register_all_handlers
register_all_handlers(app)

print("✅ Bot is starting securely...")

app.run()