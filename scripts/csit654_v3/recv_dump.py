"""Tiny localhost receiver for Amigo in-page scrape dumps (CORS enabled)."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

OUT = Path(__file__).resolve().parents[2] / "subjects" / "csit654" / "v3" / "source" / "amigo"


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(n)
        OUT.mkdir(parents=True, exist_ok=True)
        name = self.path.strip("/").replace("..", "") or "dump.json"
        if not name.endswith(".json"):
            name += ".json"
        path = OUT / name
        path.write_bytes(body)
        # also split if array
        try:
            data = json.loads(body.decode("utf-8"))
            if isinstance(data, list):
                from save_batch import save_batch

                kind = "re50" if "re50" in name else "topic"
                save_batch(data, kind)
        except Exception as e:
            (OUT / (name + ".err")).write_text(str(e), encoding="utf-8")
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == "__main__":
    port = 9877
    print(f"listening on http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
