from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.burger_links import IBurgerLinks

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IBurgerLinks)
    grok.require('zope2.View')
    grok.template('burger_links_view')
    grok.name('view')

