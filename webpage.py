import http.server
import socketserver
import threading

web_port = 8080

port_range = (3030, 3035)

class _InMemoryHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global port_range
        if self.path == '/' or self.path == '/index.html':
            with (open("index.html", "r") as f):
                html = f.read()
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

def _serve_in_background():
    with socketserver.TCPServer(("", web_port), _InMemoryHandler) as httpd:
        print(f"Serving on http://127.0.0.1:{web_port}")
        httpd.serve_forever()


def serve_webpage():
    thread = threading.Thread(target=_serve_in_background, daemon=True)
    thread.start()