import tornado.template
import tornado.ioloop
import tornado.web
import os

# home page of website
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    settings = {"template_path": os.path.join(dirname, 'templates'),
                "static_path"  : "/var/www/randygoodson.com/"}

    app =tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)
 
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
