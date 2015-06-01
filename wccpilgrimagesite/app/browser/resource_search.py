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
