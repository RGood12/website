import tornado.template
import tornado.ioloop
import tornado.web
import os
import io
import whatimage
import pyheif
from PIL import Image
import json
import qrcode, pyshorteners
import base64
from io import BytesIO
from urllib.parse import urlparse
from tornado.web import RedirectHandler, Application

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

class ToolsIndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open("templates/tools/description.json", 'r') as fh:
            d = json.load(fh)
        self.render("tools_index.html", descriptions = d)

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

class HEICHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("heic.html")
    def post(self):

        file1 = self.request.files['file1'][0]
        original_fname = file1['filename'].split(".")[0]
        original_fname = f"{original_fname}.jpeg"
        
        try:
            i = pyheif.read_heif(file1['body'])

            # Convert to other file format like jpeg
            s = io.BytesIO()
            pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
            pi.save(s, "JPEG")
        
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + original_fname)
        
            self.write(s.getvalue())
        except:
            self.render("heic_error.html")

class URLHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("url-shortener.html")
    def post(self):
       link = self.get_argument('link', None)

       short_url = pyshorteners.Shortener().tinyurl.short(link)

       self.render("url_show.html", short_url = short_url, link = link, domain = urlparse(link).netloc)

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    settings = {"template_path": os.path.join(dirname, 'templates'),
                "static_path"  : os.path.join(dirname, '/var/www/randygoodson.com/static/')}

    app =tornado.web.Application([
        (r"/", MainHandler),
        (r"/resume", ResumeHandler),
        (r"/whatido", WIDHandler),
        (r"/tools", ToolsIndexHandler),
        (r"/qr", QRHandler),
        (r"/heic", HEICHandler),
        (r"/url-shortener", URLHandler),
        (r"/certsandtrainings", CertIndexHandler),
        (r"/(certsandtrainings/[a-z_0-9]+)", CertHandler),
        (r"/projects", ProjectsIndexHandler),
        (r"/(projects/[a-z_0-9]+)", ProjectHandler),
    ], **settings)

    app.listen(8085)
    tornado.ioloop.IOLoop.current().start()
