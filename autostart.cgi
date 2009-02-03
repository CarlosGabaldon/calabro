#!/usr/bin/python
print "Content-type: text/html\r\n"
print """<html><head><META HTTP-EQUIV="Refresh" CONTENT="1; URL=/"></head><body>R$
import os
os.setpgid(os.getpid(), 0)
os.system('/usr/bin/python2.4 start-calabro.py  &')