import http.server
import socketserver
import os

PORT = 26915
directory = os.path.abspath(os.path.curdir)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if the requested file exists
        if os.path.exists(os.path.join(directory, self.path)):
            # Send the requested file if it exists
            super().do_GET()
        else:
            # Send a 404 error if the file does not exist
            self.send_error(404, "File not found", "The requested file does not exist.")

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}...")
    httpd.serve_forever()