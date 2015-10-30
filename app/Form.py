import mechanize
from urllib2 import urlopen
from urlparse import urlparse

class URL(object):
  url = ""
  
  def __init__(self, url):
    self.url = url
    #self.crawl_forms()

  def crawl_forms(self):
    try:
        res = self.br.open(self.url)
        http_message = res.info()
        if 'content-type' in http_message and http_message["content-type"] == 'text/html':
            self.saveForms()

    except (mechanize.HTTPError, mechanize.URLError):
        return

  def saveForms(self):
    for form in self.br.forms():
      formObj = Form(form.name)
      for control in form.controls:
          formObj.addElement(control.name,control.type)
    self.forms.append(formObj)

  def getForms(self,br):
    forms = []
    for form in br.forms():
      formObj = Form(form.name)
      for control in form.controls:
          formObj.addElement(control.name,control.type)
      forms.append(formObj)
    return forms

class Form:
  formName= ""
  elements = []
  def __init__(self, formName):
    self. elements = []
    self.formName = formName

  def addElement(self,elementName,elementType):
    elem = {}
    elem['Name'] = elementName
    elem['Type'] = elementType
    self.elements.append(elem.copy())
  
  def getName(self):
    return self.formName

  def getElements(self):
    return self.elements