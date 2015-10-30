from flask import render_template, flash, redirect
from collections import deque
import tldextract
import hashlib
import cPickle
import mechanize
from urllib2 import urlopen
from urlparse import urlparse
class URLManager:
  CONST_SIZE = 0
  urlList = deque()
  fileList = deque()
  urlVisitedHash = []
  domain = ""
  index = 0
  def __init__(self, url):
      CONST_SIZE = 0
      self.urlList = deque()
      self.fileList = deque()
      self.urlVisitedHash = []
      self.domain = ""
      self.index = 0
      URLManager.domain = self.getDomainName(url)
      self.putURL(url)

    
  def getURL(self):
    if(len(self.urlList) > 0):
      url = self.urlList.pop()
      self.fileList.append(url)
      return url
    else:
      self.appendToFile()
      return "end"


  def putURL(self,url):
    url = self.removeExtra(url)
    if(self.checkInDomain(url) and not self.alreadyParsed(url)):
      self.urlList.append(url)

      
  

  def appendToFile(self):
    cPickle.dump(self.fileList, open('url.p', 'wb')) 
      

  def removeFalseURL(self,url):
    self.fileList.remove(url)
    #print( "Removing :" + url)
    

  def removeExtra(self,url):
    o = urlparse(url)
    url = o[0] + "://" + o[1] + o[2]
    return url

  def is_html(self,url):
    # try:
    #print url
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    br.set_handle_refresh(False)
    res = br.open(url)
    http_message = res.info()
    flash (http_message)
    if 'content-type' in http_message and 'text/html' in http_message["content-type"]:
        return True
    return False
    # except (mechanize.HTTPError, mechanize.URLError):
    #   print mechanize.HTTPError

  def getDomainName(self,url):
    return tldextract.extract(url).domain

 
  def checkInDomain(self,url):
    if self.getDomainName(url) == URLManager.domain:
      return True
    else:
      return False

  def alreadyParsed(self,url):
    hashValue = hashlib.md5(url).hexdigest() 
    if hashValue in self.urlVisitedHash:
      return True
    else:
      self.urlVisitedHash.append(hashValue)
      return False

  def getUrlList(self):
    return cPickle.load(open('url.p', 'rb'))
    
  
