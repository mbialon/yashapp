import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
      <body>
        <form action="/format" method="post">
          <div><textarea name="snippet" rows="24" cols="80"></textarea></div>
          <div><input type="submit" value="Format"></div>
        </form>
      </body>
      </html>""")

class Format(webapp.RequestHandler):
  def post(self):
    self.response.out.write(self.request.get('snippet'))

app = webapp.WSGIApplication([('/', MainPage), ('/format', Format)], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == "__main__":
  main()
