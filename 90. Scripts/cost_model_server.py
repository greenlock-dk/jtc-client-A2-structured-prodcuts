from __future__ import annotations

import json
import mimetypes
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
VISUALS_DIR = ROOT / "07. Visutals"
INDEX_PATH = VISUALS_DIR / "index.html"
VIEWS_PATH = ROOT / "05. Cost modeling" / ".cost-model-views.json"
HOST = "127.0.0.1"
PORT = 8000

sys.path.insert(0, str(ROOT / "05. Cost modeling"))
from generate_dashboard import generate_dashboard  # noqa: E402

DEFAULT_VIEWS = {
    "current": {"visible": list(range(10)), "filters": [], "groups": [], "sorts": []},
    "position-size": {"visible": list(range(10)), "filters": [], "groups": [], "sorts": []},
}


def read_views() -> dict:
    if not VIEWS_PATH.exists():
        return DEFAULT_VIEWS.copy()
    try:
        value = json.loads(VIEWS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return DEFAULT_VIEWS.copy()
    return value if isinstance(value, dict) and value else DEFAULT_VIEWS.copy()


def write_views(value: dict) -> None:
    temporary_path = VIEWS_PATH.with_suffix(".tmp")
    temporary_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary_path.replace(VIEWS_PATH)


class CostModelHandler(BaseHTTPRequestHandler):
    def send_json(self, status: HTTPStatus, value: object) -> None:
        payload = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/views":
            self.send_json(HTTPStatus.OK, read_views())
            return
        if path == "/":
            path = "/index.html"
        requested = (VISUALS_DIR / unquote(path.lstrip("/"))).resolve()
        if requested != INDEX_PATH.resolve() or not requested.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        generate_dashboard()
        payload = requested.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(str(requested))[0] or "text/plain")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_PUT(self) -> None:
        if urlparse(self.path).path != "/api/views":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            value = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Request body must be valid JSON."})
            return
        if not isinstance(value, dict) or not value:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "At least one view is required."})
            return
        write_views(value)
        self.send_json(HTTPStatus.OK, value)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), CostModelHandler)
    print(f"Cost model dashboard: http://{HOST}:{PORT}/")
    print(f"View data: {VIEWS_PATH.relative_to(ROOT)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping cost model server")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
