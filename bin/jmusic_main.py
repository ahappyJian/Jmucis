#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: zhujian
@contact: jzhu.k.r@qq.com
@date: Sun May 31 16:45:22 CST 2015
@version: 0.0.1
@license: Copyright 
@copyright: Copyright 
"""

import os
import sys
import urllib
import SimpleHTTPServer 
import SocketServer
import time

PORT = 8080
WEBDIR = "/home/zhujian/jmusic_web"

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        os.chdir(WEBDIR)
        SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self,path)

    def do_GET(self):
        nick = self.path[1:]
	# decode 
        nick = str(urllib.unquote(nick))
        if nick != 1:
            report_html = 'Hello World!'
        else:
            report_html = 'bad call'
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", len(report_html))
        self.end_headers()
        self.wfile.write(report_html)

def GetCurTime():
	ISOTIMEFORMAT='%Y-%m-%d %X'
	return time.strftime( ISOTIMEFORMAT, time.gmtime( time.time() ) )

if __name__ == '__main__':
    try:
        httpd = SocketServer.TCPServer(("", PORT), Handler)
	timestr = GetCurTime()
        print "Jmusic startup at time:%s from dir:%s, at port:%s" \
		%(timestr, repr(WEBDIR), PORT)
        httpd.serve_forever()
    except Exception,e:
        print 'service error:',e
