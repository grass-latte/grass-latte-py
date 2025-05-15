import http.server
import socketserver
import threading

from .index import HTML_SOURCE
from .._port_range import get_port_range

DEFAULT_WEB_PORT = 8080

class _InMemoryHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            port_range = get_port_range()
            html = HTML_SOURCE
            fi = html.rfind("</body>")
            html =  html[:fi] +\
                f"  <div id=\"port-marker-he9RYeXH5Psd7vcKOzWs\" style=\"display: none;\">{port_range[0]}-{port_range[1]}</div>\n  " +\
                html[fi:]
            html = html.encode("utf-8")

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(html)))
            self.end_headers()
            self.wfile.write(html)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def log_message(self, _format, *args):
        pass


def _serve_in_background(port: int):
    with socketserver.TCPServer(("", port), _InMemoryHandler) as httpd:
        print(f"Serving on http://127.0.0.1:{port}")
        httpd.serve_forever()

def serve_webpage():
    serve_webpage_at_port(DEFAULT_WEB_PORT)

def serve_webpage_at_port(port: int):
    thread = threading.Thread(target=lambda: _serve_in_background(port), daemon=True)
    thread.start()
