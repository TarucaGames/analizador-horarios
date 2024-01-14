from http.server import BaseHTTPRequestHandler
from os import curdir
from os.path import join as pjoin
import cgi

from api.analyzer import FileAnalyzer


class handler(BaseHTTPRequestHandler):
    store_path = pjoin(curdir, "store.json")

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello, world!".encode("utf-8"))
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )
        filename = form["file"].filename
        data = form["file"].file.read()
        open("/tmp/%s" % filename, "wb").write(data)
        analyzer = FileAnalyzer()
        response = analyzer.contar_horas_trabajo("/tmp/%s" % filename)
        print("## larespuestaes: " + " ".join(response))
        self.respond("\n".join(response).encode())
        # self.respond(("uploaded %s, thanks" % filename).encode())


""" 
    def do_POST(self):
        if self.path == "/store.json":
            length = self.headers["content-length"]
            data = self.rfile.read(int(length))

            with open(self.store_path, "w") as fh:
                fh.write(data.decode())

            self.send_response(200) """


""" 
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b"This is a POST request \n")
        response.write(b"Received: ")
        response.write(body)
        self.wfile.write(response.getvalue()) """
