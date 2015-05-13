from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.resources import IResources

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IResources)
    grok.require('zope2.View')
    grok.template('resources_view')
    grok.name('view')

