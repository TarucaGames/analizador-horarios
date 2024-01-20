from http.server import BaseHTTPRequestHandler
from os import curdir
from os.path import join as pjoin
import cgi
import json

from api.analyzer import FileAnalyzer


class handler(BaseHTTPRequestHandler):
    store_path = pjoin(curdir, "store.json")

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        response_data = {"data": "ok"}
        response_string = json.dumps(response_data)
        self.respond(response_string.encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write('{"data": "Hello, world!"}'.encode("utf-8"))
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
        try:
            respuesta, response = analyzer.contar_horas_trabajo("/tmp/", filename)
            errors = []
            if response["hasErrors"]:
                errors.append("Se encontró algún error en los horarios")
            response_data = {"data": response, "errors": errors}
            response_string = json.dumps(response_data)
            self.respond(response_string.encode())
        except Exception as errorMsg:
            response_data = {"data": None, "errors": [errorMsg]}
            response_string = json.dumps(response_data)
            self.respond(response_string.encode())
        # self.respond(("uploaded %s, thanks" % filename).encode())
