from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPilgrimageSteps)
    grok.require('zope2.View')
    grok.template('pilgrimage_steps_view')
    grok.name('view')

