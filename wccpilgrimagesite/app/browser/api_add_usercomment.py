from five import grok
from plone.directives import dexterity, form
from Products.CMFCore.interfaces import IContentish
from plone import api
import json
from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps
import base64
from plone.dexterity.utils import createContentInContainer, createContent
from plone import namedfile
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import idnormalizer

grok.templatedir('templates')

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False

class api_add_usercomment(grok.View):
    grok.context(IPilgrimageSteps)
    grok.require('zope2.View')
    grok.name('add+usercomment')
    
    def __call__(self):
        request = self.request
        context = self.context
        title = ''
        email = ''
        message = ''
        parent_path = '/'.join(context.getPhysicalPath())
        # if request.form:
        #     form = request.form
        #     if 'title' in form:
        item = createContentInContainer(context, 'wccpilgrimagesite.app.usercomment', checkConstraints=False, title=u"User Comment")
        setattr(item, 'title', "User Comment")
        item.title = 'hi'
        title = 'hi'
        # if 'email' in form:
        #     item.email = form['email']
        #     email = form['email']
            
        # if 'message' in form:
        #     item.message = form['message']
        #     message = form['message']
        # id = self.generate_id(parent_path, 'user-comment')
        # if id:
        #     context.manage_renameObject(item.id, id)
        item.reindexObject()

      
        #import pdb; pdb.set_trace()
        return self._response(response={'mssg': 'Thank you for your contribution! It will appear on the website after it has been approved by one of our staff members.'})
    
    def generate_id(self, path=None, new_id=None):
        if path and new_id:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':0},portal_type='wccpilgrimagesite.app.usercomment')
            if brains:
                brain = brains[0]
                ids = brain._unrestrictedGetObject().objectIds()
                
                if new_id in ids:
                    arr1 = [x.split('-')[-1] for x in ids if x.startswith(new_id)]
                    arr2 = [int(x) for x in arr1 if is_number(x)]
                    
                    if arr2:
                        return new_id+str(max(arr2)+1)
                    else:
                        return new_id+'-1'
                else:
                    return new_id
        return None
    
    
    def _response(self, response={}, status_code=200, status_message=''):
        view_response = self.request.response
        view_response.setHeader('Content-type', 'application/json')
        view_response.setStatus(status_code, status_message)
        view_response.setBody(json.dumps(response), lock=True)

        return view_response
    
