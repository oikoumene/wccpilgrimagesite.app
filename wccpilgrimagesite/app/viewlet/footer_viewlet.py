from five import grok
from plone.directives import dexterity, form
from Products.CMFCore.interfaces import IContentish
import datetime
from plone.app.layout.viewlets.interfaces import IPortalFooter
from wccpilgrimagesite.app import MessageFactory as _

grok.templatedir('templates')

class footer_viewlet(grok.Viewlet):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)
    #grok.name('startupworks.pjp.widgets')
    
    def current_year(self):
        return datetime.datetime.now().year
    
    def world_council_churches(self):
        return _(u"World Council of Churches")
    
    def conditions_privacy_policy(self):
        return _(u"Conditions of Use & Privacy Policy")
    
    