from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.video import IVideo

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IVideo)
    grok.require('zope2.View')
    grok.template('video_view')
    grok.name('view')

