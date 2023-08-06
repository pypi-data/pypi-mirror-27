import pydoc
from pygments import highlight, lexers, formatters
import os
import json


class JsonFormatter(object):

    def __init__(self):
        pass

    def format(self, result, terminal_size):
        view = ""
        _, columns = terminal_size
        for idx, res in enumerate(result):
            view += str(idx+1)+". "+"*"*(int(columns)-4)+" \n\n"
            formatted_json = json.dumps(res, indent=2, sort_keys=True)
            colorful_json = highlight(unicode(formatted_json, 'UTF-8'),
                                      lexers.JsonLexer(),
                                      formatters.TerminalFormatter())
            view += colorful_json+"\n\n"
        return view


class PagedPresenter(object):

    def __init__(self, formatter):
        self.formatter = formatter

    def present(self, results):
        rows = results.rows()
        view = self.formatter.format(rows, os.popen('stty size', 'r').read().split())
        pydoc.pager(view)
