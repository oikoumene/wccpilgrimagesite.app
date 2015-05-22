from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.resource_upload import IResourceUpload
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IResourceUpload)
    grok.require('zope2.View')
    grok.template('resource_upload_view')
    grok.name('view')


    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def resourceUpload_result(self):
        context = self.context
        catalog = self.catalog
	path = '/'.join(context.getPhysicalPath())
	brains = catalog.searchResults(path={'query':path, 'depth':0}, portal_type='wccpilgrimagesite.app.resourceupload')
	return brains