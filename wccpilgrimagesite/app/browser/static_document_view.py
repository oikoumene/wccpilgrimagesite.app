from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.static_document import IStaticDocument

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IStaticDocument)
    grok.require('zope2.View')
    grok.template('static_document_view')
    grok.name('view')

