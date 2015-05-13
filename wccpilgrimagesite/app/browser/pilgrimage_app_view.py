from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_app import IPilgrimageApp

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPilgrimageApp)
    grok.require('zope2.View')
    grok.template('pilgrimage_app_view')
    grok.name('view')

