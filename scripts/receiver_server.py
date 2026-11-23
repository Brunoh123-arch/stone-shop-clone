import http.server
import socketserver
import os
import json
import base64

PORT = 8765
SAVE_DIR = os.path.abspath('videosprodutos')
os.makedirs(SAVE_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Filename, X-Chunk, X-Total-Chunks')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        filename = self.headers.get('X-Filename', 'downloaded_video.mp4')
        filepath = os.path.join(SAVE_DIR, filename)
        
        chunk = int(self.headers.get('X-Chunk', 0))
        mode = 'ab' if chunk > 0 else 'wb'
        
        with open(filepath, mode) as f:
            f.write(post_data)
            
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok', 'bytes': len(post_data), 'filepath': filepath}).encode('utf-8'))

print(f"Receiver server listening on port {PORT}...")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
