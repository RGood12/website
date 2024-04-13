import tornado.ioloop
import tornado.web
import os
import io
import json
import qrcode, pyshorteners
import base64
from datetime import datetime
from io import BytesIO
from urllib.parse import urlparse
from static.secrets import port
from scripts.heic_convert import heic_convert
import sys
sys.path.insert(1, '/home/randy/git/birthday-bot/')
from bd.upload_photo import *

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
        try:
            print(self.request.files.items())
            heic_convert(self, self.request.files.items())
        except Exception as e:
            print(f"{e}")
            self.render("heic_error.html")

class URLHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("url-shortener.html")
    def post(self):
       link = self.get_argument('link', None)

       short_url = pyshorteners.Shortener().tinyurl.short(link)

       self.render("url_show.html", short_url = short_url, link = link, domain = urlparse(link).netloc)

class BPHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("photo_uploader.html")
    def post(self):
        try:
            buddy_name = self.get_argument('buddy', None)
            msg = self.get_argument('message', None)
            submitter_name = self.get_argument('submitter', None)

            f = self.request.files['file'][0]
            file_body = f['body']
            file_name = f['filename']

            # Write the file to the temporary directory
            with open(file_name, 'wb') as f:
                f.write(file_body)

            # Upload the file to Google Drive using the function from google_drive.py
            file_id = upload_file(file_name, buddy_name, msg, submitter_name)
            # File uploaded successfully, remove the temporary file/directory
            os.remove(file_name)

            with open('photo.log', 'a') as file:
                timestamp = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                file.write(f"{timestamp} -  For: {buddy_name} | Message: {msg} | From: {submitter_name}\n")

            self.render("photo_upload_success.html")

        except Exception as e:
            print(e)
            self.render("heic_error.html")

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    settings = {"template_path": os.path.join(dirname, 'templates'),
                "static_path"  : os.path.join(dirname, 'static')}

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
        (r"/buddy-photo-upload", BPHandler),
    ], **settings)

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
