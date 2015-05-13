from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.resource_upload import IResourceUpload

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IResourceUpload)
    grok.require('zope2.View')
    grok.template('resource_upload_view')
    grok.name('view')

