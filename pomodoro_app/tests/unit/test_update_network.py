from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from pomodoro_app.infrastructure.update.checker import fetch_update_json


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # type: ignore[override]
        data = {"version": "9.9.9", "changelog": "x", "url": "https://example.com"}
        raw = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def test_fetch_update_json_local_server(tmp_path):
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/update.json"
        data = fetch_update_json(url, timeout=2.0)
        assert data["version"] == "9.9.9"
    finally:
        server.shutdown()


