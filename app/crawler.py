# import re
# from array import array
import mechanize
from urllib2 import HTTPError
from Manager import URLManager
import urlparse
from urllib2 import HTTPError
import socks
import socket
import cookielib
# SOCKS_PROXY_HOST = 'localhost'
# SOCKS_PROXY_PORT = 8080

br = mechanize.Browser()
obj = ""
cj = cookielib.CookieJar()
br.set_handle_robots(False)
br.set_handle_referer(False)
br.set_handle_refresh(False)
br.set_cookiejar(cj)

def login(uri):
    print "uri :" + uri
    br.open(uri)
    form = br.select_form(nr=0)
    inputs = []
    for control in br.form.controls:
      if not (control.type == "hidden" or control.type == "submit"):
        value = raw_input("Enter value for " + str(control.name) + " : ")
        elem = {}
        elem['Key'] = str(control.name)
        elem['Value'] = value
        inputs.append(elem.copy())
    i =0      
    try:
      for elem in inputs:
        br.form[elem['Key']] = elem['Value']

      br.submit()
      print br.response().read()
    except HTTPError,hError:
      print str(hError)

def crawlUrls():
    for link in br.links():
        obj.putURL(link.absolute_url)
                

def is_html(res):
    http_message = res.info()
    if 'content-type' in http_message and 'text/html' in http_message["content-type"]:
        return True

    return False


def main(uri):
    global obj
    #login(uri)
    obj =""
    obj = URLManager(uri)
    curr_url = obj.getURL()
    while curr_url != "end":
        print curr_url
        try:
            res = br.open(curr_url)
            if is_html(res):
                crawlUrls()
            else:
                obj.removeFalseURL(curr_url)
            curr_url = obj.getURL()

        except (mechanize.HTTPError, mechanize.URLError):
            obj.removeFalseURL(curr_url)
            curr_url = obj.getURL()
    print "no of url: " + str(len(obj.getUrlList()))
    return obj

