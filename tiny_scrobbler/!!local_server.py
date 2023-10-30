 
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/callback'):
            query = urlparse(self.path).query
            params = parse_qs(query)
            
            token = params.get('token', [None])[0]
            
            if token:
                # Process the token, exchange it for a session key, etc.
                # Store it or use it as required by your application.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization successful!")
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization failed or was canceled.")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', YOUR_CHOSEN_PORT)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f'Serving on port {YOUR_CHOSEN_PORT}')
    httpd.serve_forever()
