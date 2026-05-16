#!/usr/bin/env python3
"""
Printify local proxy — run this on your machine so cloud sessions can
reach Printify through your residential IP.

Usage:
    python proxy.py

Then expose it (free, no signup, just SSH):
    Mac/Linux:  ssh -R 80:localhost:8765 nokey@localhost.run
    Windows:    ssh -R 80:localhost:8765 nokey@localhost.run

Copy the https://... URL it prints, paste it into PRINTIFY_BASE_URL in
the cloud session's .env file, then all scripts will route through here.

Stop with Ctrl+C.
"""

import sys
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

TARGET = "https://api.printify.com"
PORT   = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

STRIP_REQ_HEADERS  = {"host", "content-length", "transfer-encoding"}
STRIP_RESP_HEADERS = {"transfer-encoding", "connection"}


class ProxyHandler(BaseHTTPRequestHandler):
    def forward(self):
        url = TARGET + self.path
        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length) if length else None
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in STRIP_REQ_HEADERS}

        req = urllib.request.Request(url, data=body, headers=headers, method=self.command)
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in STRIP_RESP_HEADERS:
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in STRIP_RESP_HEADERS:
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = forward

    def log_message(self, fmt, *args):
        print(f"  {self.command:<6} {self.path[:60]:<60} {args[1]}")


if __name__ == "__main__":
    print(f"\n  Printify proxy listening on http://localhost:{PORT}")
    print(f"  Forwarding to {TARGET}\n")
    print(f"  Expose it (free):")
    print(f"    ssh -R 80:localhost:{PORT} nokey@localhost.run\n")
    print(f"  Then set in cloud .env:")
    print(f"    PRINTIFY_BASE_URL=https://<your-id>.localhost.run/v1\n")
    print("  Ctrl+C to stop.\n")
    print("  " + "-" * 66)
    HTTPServer(("", PORT), ProxyHandler).serve_forever()
