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
from plone.i18n.normalizer import idnormalizer

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
        church = ''
        parent_path = '/'.join(context.getPhysicalPath())
        if request.form:
            form = request.form
            if 'name' in form:
                item = createContentInContainer(context, 'wccpilgrimagesite.app.resourceupload', checkConstraints=False, title=u"Resource Upload")
                setattr(item, 'title', "Resource Upload")
                item.name = form['name']
                name = form['name']
                
                
                if 'email' in form:
                    item.email = form['email']
                    
                if 'church' in form:
                    item.church = form['church']
                    church = form['church']
                    
                if 'message' in form:
                    item.message = form['message']
                    
                if 'video' in form:
                    item.video = form['video']
                    if form['video']:
                        video_item = createContentInContainer(context, 'wccpilgrimagesite.app.video', checkConstraints=False, title=form['name']+' Video')
                        
                        video_item.title = name
                        video_item.url_youtube = form['video']
                        video_item.church = church
                        
                        video_id = self.generate_id(parent_path, str(idnormalizer.normalize(form['name']+' Video')))
                        if video_id:
                            context.manage_renameObject(video_item.id, video_id)
                        video_item.reindexObject()
                    
                if 'sound' in form:
                    item.sound = form['sound']
                    if form['sound']:
                        sound_item = createContentInContainer(context, 'wccpilgrimagesite.app.sound', checkConstraints=False, title=form['name']+' Sound')
                        
                        sound_item.title = name
                        sound_item.soundcloud_id = form['sound']
                        sound_item.church = church
                        
                        sound_id = self.generate_id(parent_path, str(idnormalizer.normalize(form['name']+' Sound')))
                        if sound_id:
                            context.manage_renameObject(sound_item.id, sound_id)
                        sound_item.reindexObject()
                    
                if 'docName' in form and 'docData' in form:
                    item.document = namedfile.NamedBlobFile(
                        base64.b64decode(form['docData'].split(';base64,')[1]),
                        filename = form['docName'].decode('utf-8', 'ignore')
                    )
                    doc_item = createContentInContainer(context, 'wccpilgrimagesite.app.staticdocument', checkConstraints=False, title=form['name']+' Document')
                    doc_item.title = name
                    doc_item.church = church
                    doc_item.file = namedfile.NamedBlobFile(
                        base64.b64decode(form['docData'].split(';base64,')[1]),
                        filename = form['docName'].decode('utf-8', 'ignore')
                    )
                    doc_id = self.generate_id(parent_path, str(idnormalizer.normalize(form['name']+' Document')))
                    if doc_id:
                        context.manage_renameObject(doc_item.id, doc_id)
                    doc_item.reindexObject()
                    
                id = self.generate_id(parent_path, 'resource-upload')
                if id:
                    context.manage_renameObject(item.id, id)
                item.reindexObject()
                
                
                
            
        #import pdb; pdb.set_trace()
        return self._response(response={'mssg': 'Thank you for your contribution! It will appear on the website after it has been approved by one of our staff members.'})
    
    def generate_id(self, path=None, new_id=None):
        if path and new_id:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':0})
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
    
