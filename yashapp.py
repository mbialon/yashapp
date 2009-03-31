import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.lexers import get_all_lexers
from pygments.formatters import HtmlFormatter

class MainPage(webapp.RequestHandler):
  def get(self):
    lexer_options = "".join(sorted('<option value="' + lex[1][0] + '">' + lex[0] + '</option>' for lex in get_all_lexers()))
    self.response.out.write("""
      <html>
      <head>
        <script src="http://www.google.com/jsapi"></script>
        <script>
          google.load("jquery", "1.3");
          google.setOnLoadCallback(function() {
            $("input#execute_format").click(function() {
              var snippet = $("#snippet").val();
              var lexer = $("select").val();
              $.post("/format",
                { snippet: snippet, lexer: lexer },
                function(data) {
                  $("#formatted_snippet").text(data);
                  $("#preview_formatted_snippet").html(data);
                });
              return false;
            });
          });
        </script>
        <style>
.highlight .hll { background-color: #ffffcc }
.highlight  { background: #f8f8f8; }
.highlight .c { color: #408080; font-style: italic } /* Comment */
.highlight .err { border: 1px solid #FF0000 } /* Error */
.highlight .k { color: #008000; font-weight: bold } /* Keyword */
.highlight .o { color: #666666 } /* Operator */
.highlight .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #BC7A00 } /* Comment.Preproc */
.highlight .c1 { color: #408080; font-style: italic } /* Comment.Single */
.highlight .cs { color: #408080; font-style: italic } /* Comment.Special */
.highlight .gd { color: #A00000 } /* Generic.Deleted */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gr { color: #FF0000 } /* Generic.Error */
.highlight .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.highlight .gi { color: #00A000 } /* Generic.Inserted */
.highlight .go { color: #808080 } /* Generic.Output */
.highlight .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.highlight .gt { color: #0040D0 } /* Generic.Traceback */
.highlight .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: #008000 } /* Keyword.Pseudo */
.highlight .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: #B00040 } /* Keyword.Type */
.highlight .m { color: #666666 } /* Literal.Number */
.highlight .s { color: #BA2121 } /* Literal.String */
.highlight .na { color: #7D9029 } /* Name.Attribute */
.highlight .nb { color: #008000 } /* Name.Builtin */
.highlight .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.highlight .no { color: #880000 } /* Name.Constant */
.highlight .nd { color: #AA22FF } /* Name.Decorator */
.highlight .ni { color: #999999; font-weight: bold } /* Name.Entity */
.highlight .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.highlight .nf { color: #0000FF } /* Name.Function */
.highlight .nl { color: #A0A000 } /* Name.Label */
.highlight .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.highlight .nt { color: #008000; font-weight: bold } /* Name.Tag */
.highlight .nv { color: #19177C } /* Name.Variable */
.highlight .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.highlight .w { color: #bbbbbb } /* Text.Whitespace */
.highlight .mf { color: #666666 } /* Literal.Number.Float */
.highlight .mh { color: #666666 } /* Literal.Number.Hex */
.highlight .mi { color: #666666 } /* Literal.Number.Integer */
.highlight .mo { color: #666666 } /* Literal.Number.Oct */
.highlight .sb { color: #BA2121 } /* Literal.String.Backtick */
.highlight .sc { color: #BA2121 } /* Literal.String.Char */
.highlight .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.highlight .s2 { color: #BA2121 } /* Literal.String.Double */
.highlight .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.highlight .sh { color: #BA2121 } /* Literal.String.Heredoc */
.highlight .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.highlight .sx { color: #008000 } /* Literal.String.Other */
.highlight .sr { color: #BB6688 } /* Literal.String.Regex */
.highlight .s1 { color: #BA2121 } /* Literal.String.Single */
.highlight .ss { color: #19177C } /* Literal.String.Symbol */
.highlight .bp { color: #008000 } /* Name.Builtin.Pseudo */
.highlight .vc { color: #19177C } /* Name.Variable.Class */
.highlight .vg { color: #19177C } /* Name.Variable.Global */
.highlight .vi { color: #19177C } /* Name.Variable.Instance */
.highlight .il { color: #666666 } /* Literal.Number.Integer.Long */
        </style>
      <body>
        <h1>Yet Another Syntax Highlighter</h1>
        <form action="/format" method="post">
          <div><textarea id="snippet" name="snippet" rows="16" cols="80"></textarea></div>
          <div>
            <select name="lexer">""" + lexer_options + """</select>
            <input id="execute_format" type="submit" value="Format">
          </div>
          <div><textarea id="formatted_snippet" rows="16" cols="80"></textarea></div>
          <div id="preview_formatted_snippet"></div>
        </form>
      </body>
      </html>""")

class Format(webapp.RequestHandler):
  def post(self):
    snippet = self.request.get('snippet')
    lexer_name = self.request.get('lexer')
    f = SnippetFormatter(snippet, lexer_name)
    self.response.out.write(f.format())
    #self.response.out.write(f.get_style_defs())

class SnippetFormatter:
  def __init__(self, snippet, lexer_name):
    self.snippet = snippet
    self.lexer_name = lexer_name

  def format(self):
    return highlight(self.snippet, self.lexer(), self.formatter())

  def get_style_defs(self):
    return self.formatter().get_style_defs('.highlight')

  def lexer(self):
    return get_lexer_by_name(self.lexer_name, stripall=True)

  def formatter(self):
    return HtmlFormatter()

app = webapp.WSGIApplication([('/', MainPage), ('/format', Format)], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == "__main__":
  main()
