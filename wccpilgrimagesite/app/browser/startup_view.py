from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.interfaces import IContentish
from plone.app.multilingual.interfaces import ILanguageRootFolder

grok.templatedir('templates')

class startup_view(grok.View):
    grok.context(ILanguageRootFolder)
    grok.require('zope2.View')
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    def pilgrimagestep_app(self):
        brains = self.catalog.unrestrictedSearchResults(path={'query':'/'.join(self.context.getPhysicalPath()), 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimageapp')
        if brains:
            return brains[0]
        return None