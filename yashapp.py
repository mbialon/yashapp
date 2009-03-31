import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


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
    f = SnippetFormatter(snippet)
    self.response.out.write(f.format())

class SnippetFormatter:
  def __init__(self, snippet):
    self.snippet = snippet

  def format(self):
    return highlight(self.snippet, self.lexer(), self.formatter())

  def lexer(self):
    return get_lexer_by_name("html", stripall=True)

  def formatter(self):
    return HtmlFormatter(lineos=True)

app = webapp.WSGIApplication([('/', MainPage), ('/format', Format)], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == "__main__":
  main()
