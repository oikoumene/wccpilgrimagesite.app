from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.sound import ISound

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ISound)
    grok.require('zope2.View')
    grok.template('sound_view')
    grok.name('view')

