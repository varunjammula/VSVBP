import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import socket
import xml.dom.minidom as XY
import os
import xml
from HTMLParser import HTMLParser
import cPickle
import Form
import re
import sys
from crawler import main
import xml.etree.ElementTree as ET
from flask import Markup
from flask import render_template, flash, redirect,jsonify

reload(sys)
sys.setdefaultencoding('utf8')
#SOCKS_PROXY_HOST = '127.0.0.1'
#SOCKS_PROXY_PORT = 8080

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def chkSQLInjection(opstring):

    flash("Analyzing response... You will be notified if vulnerability found")
    # tree = ET.parse('app/errors.xml')
    # root=tree.getroot()
    # errorList=root.findall('error')
    tree = XY.parse('app/errors.xml')
    errorList= tree.getElementsByTagName("error")
    i=0
    flag=0
    # file = open('Output.txt', 'r')
    for line in errorList:
        error=(str(errorList[i].attributes["regexp"].value))
        i=i+1
        if re.search(error,opstring):
           flash ("Possible SQL vulnerability ")
           flag=1

    return flag

#
# def create_connection(address, timeout=None, source_address=None):
#     sock = socks.socksocket()
#     sock.connect(address)
#     return sock


def SQL_Module(obj):
    flash("------------------------------Running SQL Module----------------------------------------------------")
    socks_enable=0;
    #Create a browser
    ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)'
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    br.addheaders = [('User-Agent', ua), ('Accept', '*/*')]

    # tree = ET.parse('app/sqlAttacks.xml')
    tree = XY.parse('app/sqlAttacks.xml')
    attackList= tree.getElementsByTagName('attack')
    xml_attackName = tree.getElementsByTagName('name')
    xml_attack = tree.getElementsByTagName('code')
    # root=tree.getroot()

    try:
        for list in obj.getUrlList():
            i=0
            flash ("Trying SQL attacks on URL: "+list)
            page= br.open(list)

            #Get list of forms
            urlObj=Form.URL(list)
            forms = urlObj.getForms(br)


            #loop through the forms
            for attack in attackList:
                message = Markup("<hr><center><h3>Trying " + str(xml_attackName[i].firstChild.nodeValue)+" attack </h3></center>")
                flash ( message)
                attack=(str(xml_attack[i].firstChild.nodeValue))
                form_number=0
                for form in forms:
                    # form_name=fe.getName()
                    br.select_form(nr=form_number)
                    br.form.set_all_readonly(False)
                    #loop through elements in form
                    for elem in form.getElements():
                        element_name=str(elem["Name"])
                        # print(element_name)
                        br[element_name]=attack
                    form_number=form_number+1
                res = br.submit()
                content=strip_tags(res.read());
                # flash ("Analysing Response...")
                content=os.linesep.join([s for s in content.splitlines() if s])
                #flash (content)
                reval=chkSQLInjection(content)
                i=i+1;
                br.back()
    except:
        flash("Link in infinite redirect")
        pass
#Reference
#http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python