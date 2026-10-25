"""Local HTTP server with canned responses for test-check-data-sources.sh.

Binds to a free port on 127.0.0.1 and prints the port on the first line of stdout.
"""
import http.server
import json
import sys

FEATURE_COLLECTION = json.dumps({"type": "FeatureCollection", "features": []})

CORS = {"Access-Control-Allow-Origin": "*"}

# path -> (status, extra headers, body)
ROUTES = {
    "/geojson": (200, CORS, FEATURE_COLLECTION),
    "/no-cors": (200, {}, FEATURE_COLLECTION),
    "/html": (200, CORS, "<html><body>Service unavailable</body></html>"),
    "/json": (200, CORS, json.dumps({"id": "FOLK1A"})),
    "/style": (200, CORS, json.dumps({"version": 8, "sources": {}, "layers": []})),
    "/tiles/0/0/0.pbf": (200, CORS, b"\x1a\x00"),
    "/busy": (503, CORS, "at capacity"),
    "/other-origin": (200, {"Access-Control-Allow-Origin": "https://kort.example.dk"}, FEATURE_COLLECTION),
}


# Requests seen per path, for routes that change answer over time.
seen = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def respond(self, *response):
        status, headers, body = response or ROUTES.get(self.path, (404, {}, "not found"))
        data = body.encode() if isinstance(body, str) else body
        self.send_response(status)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        seen[self.path] = seen.get(self.path, 0) + 1
        if self.path == "/busy-once" and seen[self.path] == 1:
            return self.respond(503, CORS, "at capacity")
        if self.path == "/busy-once":
            return self.respond(200, CORS, FEATURE_COLLECTION)
        if self.path in ("/tilejson", "/tilejson-broken"):
            folder = "tiles" if self.path == "/tilejson" else "missing"
            port = self.server.server_address[1]
            template = f"http://127.0.0.1:{port}/{folder}/{{z}}/{{x}}/{{y}}.pbf"
            return self.respond(200, CORS, json.dumps({"tiles": [template]}))
        self.respond()

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/overpass" and body.startswith(b"data="):
            return self.respond(200, CORS, json.dumps({"elements": []}))
        self.respond()

    def log_message(self, *args):
        pass


server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
print(server.server_address[1], flush=True)
sys.stdout.close()
server.serve_forever()
