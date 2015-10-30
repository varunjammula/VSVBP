
from flask import render_template, flash, redirect
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
import requests
from bs4 import BeautifulSoup
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
from urlparse import urlparse
from crawler import main
from Manager import URLManager
import xml.etree.ElementTree as ET

br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
tree = ET.parse('app/xssAttacks.xml')
root=tree.getroot()

def XSS_Module(obj):
	flash("------------------------------Running XSS Module----------------------------------------------------")
	urlno=0;
 	for eachurl in obj.getUrlList():
 		urlno=urlno+1
 		flash ("Verifying the URL: "+eachurl)
 		source_code = requests.get(eachurl,verify=False)
 		plain_text = source_code.text
 		soup_re = BeautifulSoup(plain_text)
 		match=soup_re.body.findAll(text='XSS by jammula')
 		if len(match)>0 :
 			flash("You've been hacked !")

 		soup = BeautifulSoup(plain_text)
 		forms_page=soup.findAll('form')
 		forms_number= len(forms_page)
		#flash(forms_number)
 		if forms_number>0:
 		    for i in range(0,forms_number):
 		    	anum=0
 		        for attack in root.findall('attack'):
 		            code = attack.find('code').text
 		            anum=anum+1
 		            code=str(code)

 		            input=forms_page[i].findAll('input')
 		            br.open(eachurl)
 		            br.select_form(nr=i)
 		            flag=0;
 		            for inp in input:
  		                if inp['type']=='text':
  		                    if inp['name']=='email' or inp['name']=="Email":
  		                        br.form[inp['name']]='test@test.com'
  		                    br.form[inp['name']]=code
  		                if inp['type']=='checkbox':
  		                	print inp['name']
  		                if inp['type']=='button' or inp['type']=='submit' or inp['type']=='reset':
  		                	flag=1;
  		            if flag==1:
  		            	br.submit()
  		            else:
  		            	break;
 		            #flash(br.response().read())
 		            #br.back()
 		            soup_response = BeautifulSoup(br.response().read())
 		            match=soup_response.body.findAll('script',{"id" : "injected"})
 		            text_match=soup_response.body.findAll(text='XSS by jammula')
 		            #print text_match
 		            if len(match)>0 or len(text_match)>0:
 		            	flash( "------------------------------------------")
 		             	flash( "Injected code: "+code)
 		                flash("Response: Yo! you have been hacked!")
#  		            else:
#  		                flash("Response: Injection failed, injecting another one!")
 		            br.back()

 		else:
 			#flash("Check input fields !")
 			input_page=soup.findAll('input')
 			for inp in input_page:
 				flash(inp)
 				flag=0;
 				for attack in root.findall('attack'):
 					code = attack.find('code').text
 					code=str(code)
	  		        if inp['type']=='text':
	  		            if inp['name']=='email' or inp['name']=="Email":
	  		                br.form[inp['name']]='test@test.com'
	  		            br.form[inp['name']]=code
	  		            if inp['type']=='button' or inp['type']=='submit' or inp['type']=='reset':
	  		                flag=1;
	  		        if flag==1:
	  		            br.submit()
	  		        else:
	  		            break;
 		        	soup_response = BeautifulSoup(br.response().read())
 		        	flash(soup_response)
 		         	text_match=soup_response.body.findAll(text='XSS by jammula')
 		         	if len(match)>0 or len(text_match)>0:
 		         		flash( "------------------------------------------")
 		             	flash( "Injected code: "+code)
 		                flash("Response: Yo! you have been hacked!")

 		          	br.back()


