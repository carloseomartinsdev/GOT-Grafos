import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.js': 'application/javascript',
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor rodando em http://localhost:{PORT}")
    print(f"Abra: http://localhost:{PORT}/visualizador.html")
    print("Pressione Ctrl+C para parar")
    httpd.serve_forever()
