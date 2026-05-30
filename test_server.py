# test_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy', 'version': 'TEST'}).encode())
        elif self.path == '/api/test':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'Test server works!'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[TEST] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8088), TestHandler)
    print("TEST SERVER STARTED ON PORT 8088")
    print("Test endpoints: /api/health, /api/test")
    server.serve_forever()
