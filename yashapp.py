import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
      <head>
        <script src="http://www.google.com/jsapi"></script>
        <script>
          google.load("jquery", "1.3");
          google.setOnLoadCallback(function() {
            $("input#execute_format").click(function() {
              var snippet = $("#snippet").val();
              $.post("/format",
                { snippet: snippet },
                function(data) {
                  $("#formatted_snippet").text(data);
                  $("#preview_formatted_snippet").html(data);
                });
              return false;
            });
          });
        </script>
      <body>
        <form action="/format" method="post">
          <div><textarea id="snippet" name="snippet" rows="10" cols="80"></textarea></div>
          <div><input id="execute_format" type="submit" value="Format"></div>
          <div><textarea id="formatted_snippet" rows="10" cols="80"></textarea></div>
          <div id="preview_formatted_snippet"></div>
        </form>
      </body>
      </html>""")

class Format(webapp.RequestHandler):
  def post(self):
    snippet = self.request.get('snippet')
    formatted_snippet = snippet 
    self.response.out.write(formatted_snippet)

app = webapp.WSGIApplication([('/', MainPage), ('/format', Format)], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == "__main__":
  main()
