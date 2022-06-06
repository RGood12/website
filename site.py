import tornado.template
import tornado.ioloop
import tornado.web
import os
import json
import qrcode
import base64
from io import BytesIO
from urllib.parse import urlparse

# home page of website
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ResumeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("resume.html")

class WIDHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("WID.html")

class CertIndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open("templates/certsandtrainings/description.json", 'r') as fh:
            d = json.load(fh)
        self.render("certsandtrainings_index.html", descriptions = d)

class CertHandler(tornado.web.RequestHandler):
    def get(self, filename):
       self.render(f"{filename}.html")

class ProjectsIndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open("templates/projects/description.json", 'r') as fh:
            d = json.load(fh)
        self.render("projects_index.html", descriptions = d)

class ProjectHandler(tornado.web.RequestHandler):
    def get(self, filename):
       self.render(f"{filename}.html")

class QRHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("qr.html")
    def post(self):
       link = self.get_argument('link', None)

       img = qrcode.make(link)

       # writing QR code to base64 string to display
       buffered = BytesIO()
       img.save(buffered, format="JPEG")
       qr_str =  base64.b64encode(buffered.getvalue())

       self.render("qr_show.html", qr_str = qr_str, link = link, domain = urlparse(link).netloc)

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    settings = {"template_path": os.path.join(dirname, 'templates'),
                "static_path"  : os.path.join(dirname, '/var/www/randygoodson.com/static/')}

    app =tornado.web.Application([
        (r"/", MainHandler),
        (r"/resume", ResumeHandler),
        (r"/whatido", WIDHandler),
        (r"/qr", QRHandler),
        (r"/certsandtrainings", CertIndexHandler),
        (r"/(certsandtrainings/[a-z_0-9]+)", CertHandler),
        (r"/projects", ProjectsIndexHandler),
        (r"/(projects/[a-z_0-9]+)", ProjectHandler),
    ], **settings)

    app.listen(8085)
    tornado.ioloop.IOLoop.current().start()
