import http.server
import socketserver
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="public", **kwargs)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor rodando em http://localhost:{PORT}")
        print(f"Diretorio: {os.path.abspath('public')}")
        print("Pressione Ctrl+C para parar")
        httpd.serve_forever()
