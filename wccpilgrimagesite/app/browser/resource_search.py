from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_app import IPilgrimageApp
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class resource_search(dexterity.DisplayForm):
    grok.context(IPilgrimageApp)
    grok.require('zope2.View')
    grok.template('resource_search')

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    #pilgrimage steps

    def pilgrimage_steps(self):
        results = [{'value':'All', 'name':'All'}]
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps', review_state= 'published')
        for brain in brains:
            results.append({'value':brain.UID,
                            'name':brain.Title})
        return results

    #resource type
    #keyword (title or description)

    def searchedValue(self, val=None):
        request = self.request
        if request.form:
            return request.form[val]
        return  
