"""ROOT HTTP Server.
    The server is based on 
"""


__version__ = "0.1"

__all__ = ["RootHTTPRequestHandler"]

import os
import glob
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import ROOT
from StringIO import StringIO


def IsSubclass(obj,cls):
    if not obj: return False
    return bool(obj.Class().GetBaseClass(cls))


class RootHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    server_version = "RootHTTP/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            shutil.copyfileobj(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def mk_file_string(self,f,rootobj):
        f.write("<title>ROOT directory listing for %s</title>\n" % self.path)
        f.write("<h2>ROOT directory listing for %s</h2>\n" % self.path)
        f.write("<hr>\n<ul>\n")
        for key in rootobj.GetListOfKeys():
            displayname = linkname = cgi.escape(key.GetTitle())
            f.write('<li><b>%s:</b> <a href="%s/">%s/</a>\n' % (key.GetClassName(),linkname, displayname))
        f.write("</ul>\n<hr>\n")

    def mk_tree_string(self,f,rootobj):
        f.write("<title>TTree listing for %s</title>\n" % self.path)
        f.write("<h2>TTree listing for %s</h2>\n" % self.path)
        f.write("<hr>\n<ul>\n")
        for l in rootobj.GetListOfLeaves():
            f.write('<li>%s: <b>%s</b>\n' % (l.GetName(),l.GetTypeName()))
        f.write("</ul>\n<hr>\n")

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path): return self.list_directory(path)
        print path
        if path.find(".root") == -1: 
            self.send_error(404, "Either directory or \".root\" filename are allowed")
            return None
         
        fname, inroot = path.split(".root")
        fname += ".root"
        tfile = ROOT.TFile(fname)
        if not tfile.IsOpen():
            self.send_error(404, "Cannot open \"%s\"" % fname)
            return None

        inroot = inroot[1:]
        rootobj = tfile.Get(inroot) if inroot else tfile

        ## making a html presentaion of the root obj
        f = StringIO()

        if IsSubclass(rootobj, "TDirectory"):
            self.mk_file_string(f,rootobj)
        
        if IsSubclass(rootobj, "TTree"):
            self.mk_tree_string(f,rootobj)
        
        f.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        return f

    def list_directory(self, path):
        try:
            dirlist = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        dirs  = [f for f in dirlist if os.path.isdir(os.path.join(path,f))]
        roots = [f for f in dirlist if f.endswith(".root")]
        
        dirs.sort(lambda a, b: cmp(a.lower(), b.lower()))
        roots.sort(lambda a, b: cmp(a.lower(), b.lower()))

        f = StringIO()
        f.write("<title>Directory listing for %s</title>\n" % self.path)
        f.write("<h2>Directory listing for %s</h2>\n" % self.path)
        f.write("<hr>\n<ul>\n")
        for name in dirs+roots:
            fullname = os.path.join(path, name)
            displayname = linkname = name = cgi.escape(name)
            f.write('<li><a href="%s/">%s/</a>\n' % (linkname, displayname))
        f.write("</ul>\n<hr>\n")
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return f

    def translate_path(self, path):
        paath = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

def test(HandlerClass = RootHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
