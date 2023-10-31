from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from html import auth_result
# from pylastC import last

class StoppableServer(HTTPServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_stopped = False

    def serve_forever(self, *args, **kwargs):
        while not self.is_stopped:
            self.handle_request()

    def stop(self):
        self.is_stopped = True

class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/callback'):
            query = urlparse(self.path).query
            params = parse_qs(query)
            
            token = params.get('token', [None])[0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(auth_result(token != None).encode('utf-8'))
            self.server.stop() 
            # return token #USELESS
        else:
            self.send_response(404)
            self.end_headers()
        # !!! else if self.path.startswith('/icon.png'): ###
    

def run_server(port):

    global httpd    
    server_address = ('', port)
    httpd = StoppableServer(server_address, CallbackHandler)
    print(f'Serving on port {port}')
    httpd.serve_forever()

def stop_server():
    print('server stop')
    global httpd
    if httpd:
        # httpd.shutdown()
        httpd.stop()
        httpd = None