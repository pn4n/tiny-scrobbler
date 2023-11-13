from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading
from window import handle_error

import config

class StoppableServer(HTTPServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_stopped = False

    def serve_forever(self):
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
            print('token in callback:',token)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result_as_html(token != None).encode('utf-8'))
            config.TOKEN = token
            global httpd
            if httpd:
                httpd.stop()
                httpd = None
                print('server stopped inside callback')
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

@handle_error
def try_run_server():
	start_port = 8000 	#1024
	end_port = 10000 	#49151

	for i in range(start_port, end_port):
		try:
			t = threading.Thread(target=run_server, args=(i,))
			t.start()
			return i
		except OSError:
			pass
	raise Exception(f'No available port [ {start_port} - {end_port} ]')

def result_as_html(got_token):
    info = '<h1>Authorization successful!</h1> \
            <p>You can close this window and return to the application</p>' \
            if got_token else \
            '<h1>Authorization failed!</h1>\
             <p>Something went wrong. Please try again</p>'
    
    return (f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tiny Scrobbler</title>
</head>
<body>
    {info}
</body>
<style>
    body {{
        background-color: #252526;
        font-family: Helvetica;
        color: white;
        font-size: large;
        text-align: center;
    }}
    h1 {{
        color: #d51007;
        font-size: xx-large;
    }}
</style>
</html>
''')