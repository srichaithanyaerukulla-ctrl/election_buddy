import http.server
import socketserver
import json
import os

# FORCE current directory to the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

PORT = 8000

class ElectionBuddyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Redirect root to index.html
        if self.path == '/':
            self.path = '/frontend/index.html'
        
        # If the file isn't found in root, check the frontend folder
        elif not self.path.startswith('/frontend/'):
            clean_path = self.path.lstrip('/')
            if not os.path.exists(os.path.join(ROOT_DIR, clean_path)):
                frontend_path = os.path.join(ROOT_DIR, 'frontend', clean_path)
                if os.path.exists(frontend_path):
                    self.path = '/frontend/' + clean_path

        # Handle API simulation
        if self.path == '/crowd':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            booths = [
                {"id": "B001", "name": "Primary School East", "status": "Low", "wait_time": "10 mins"},
                {"id": "B002", "name": "Community Center North", "status": "Medium", "wait_time": "30 mins"},
                {"id": "B003", "name": "Govt High School South", "status": "High", "wait_time": "1 hour+"}
            ]
            self.wfile.write(json.dumps({"booths": booths}).encode())
            return
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "response": "Namaste! This is a **Local Preview Mode**. To use the full AI features with Gemini, please deploy to Google Cloud using the commands in the README."
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/log':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), ElectionBuddyHandler) as httpd:
    print(f"Election Buddy LOCAL PREVIEW is running!")
    print(f"Open your browser to: http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop.")
    httpd.serve_forever()
