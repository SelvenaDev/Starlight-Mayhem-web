#!/usr/bin/env python3
"""Concurrent local HTTP server for the Starlight Mayhem HTML5 preview."""
from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class PreviewHandler(SimpleHTTPRequestHandler):
    def setup(self):
        super().setup()
        # Large media and slow local disks should not cause early socket timeouts.
        self.connection.settimeout(180)

    def log_message(self, fmt, *args):
        # Suppress hundreds of successful asset requests; keep errors visible.
        status = next((int(arg) for arg in args if str(arg).isdigit()), 200)
        if status >= 400:
            super().log_message(fmt, *args)


class PreviewServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128


def main():
    parser = ArgumentParser(description="Serve the Starlight Mayhem HTML5 preview locally.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: localhost only)")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port (default: 8080)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    handler = partial(PreviewHandler, directory=str(root))
    server = PreviewServer((args.host, args.port), handler)
    print(f"Serving {root} at http://{args.host}:{args.port}/ (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping preview server.", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
