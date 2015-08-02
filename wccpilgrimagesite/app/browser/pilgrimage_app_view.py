from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_app import IPilgrimageApp
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPilgrimageApp)
    grok.require('zope2.View')
    grok.template('pilgrimage_app_view')
    grok.name('view')
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def pilgrimage_steps(self):
        results = []
        path = '/'.join(self.context.getPhysicalPath())
        brains = self.catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps')
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            parent = obj.aq_parent
            data = {'position':parent.getObjectPosition(brain.id) + 1}
            data['title'] = brain.Title
            data['url'] = brain.getURL()
            data['obj'] = obj
            data['image'] = obj.image
            data['uid'] = brain.UID
            
            results.append(data)
        if results:
            results.sort(key=lambda result:result['position'])
        return results
            
        
    

