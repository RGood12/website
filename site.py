import tornado.template
import tornado.ioloop
import tornado.web
import os

# home page of website
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ResumeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("resume.html")

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    settings = {"template_path": os.path.join(dirname, 'templates'),
                "static_path"  : os.path.join(dirname, 'static')}

    app =tornado.web.Application([
        (r"/", MainHandler),
        (r"/resume", ResumeHandler),
    ], **settings)
 
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
