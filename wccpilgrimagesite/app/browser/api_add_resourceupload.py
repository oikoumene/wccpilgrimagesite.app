from five import grok
from plone.directives import dexterity, form
from Products.CMFCore.interfaces import IContentish
from plone import api
import json
from wccpilgrimagesite.app.content.resources import IResources
import base64
from plone.dexterity.utils import createContentInContainer, createContent
from plone import namedfile
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False

class api_add_resourceupload(grok.View):
    grok.context(IResources)
    grok.require('zope2.View')
    grok.name('add+resourceupload')
    
    def __call__(self):
        request = self.request
        context = self.context
        name = ''
        if request.form:
            form = request.form
            if 'name' in form:
                item = createContentInContainer(context, 'wccpilgrimagesite.app.resourceupload', checkConstraints=False, title=u"Resource Upload")
                setattr(item, 'title', "Resource Upload")
                item.name = form['name']
                if 'email' in form:
                    item.email = form['email']
                if 'church' in form:
                    item.church = form['church']
                if 'message' in form:
                    item.message = form['message']
                if 'video' in form:
                    item.video = form['video']
                if 'sound' in form:
                    item.sound = form['sound']
                if 'docName' in form and 'docData' in form:
                    item.document = namedfile.NamedBlobFile(
                        base64.b64decode(form['docData'].split(';base64,')[1]),
                        filename = form['docName'].decode('utf-8', 'ignore')
                    )
                id = self.generate_id('/'.join(item.getPhysicalPath()[:-1]))
                if id:
                    context.manage_renameObject(item.id, id)
                item.reindexObject()
            
        #import pdb; pdb.set_trace()
        return self._response(response={'mssg': 'Thank you for your contribution! It will appear on the website after it has been approved by one of our staff members.'})
    
    def generate_id(self, path=None):
        if path:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':0})
            if brains:
                brain = brains[0]
                ids = brain._unrestrictedGetObject().objectIds()
                
                if 'resource-upload' in ids:
                    arr1 = [x.split('-')[-1] for x in ids if x.startswith('resource-upload')]
                    arr2 = [int(x) for x in arr1 if is_number(x)]
                    
                    if arr2:
                        return "resource-upload-"+str(max(arr2)+1)
                    else:
                        return "resource-upload-1"
                else:
                    return "resource-upload"
        return None   
    
    def _response(self, response={}, status_code=200, status_message=''):
        view_response = self.request.response
        view_response.setHeader('Content-type', 'application/json')
        view_response.setStatus(status_code, status_message)
        view_response.setBody(json.dumps(response), lock=True)

        return view_response
    
