from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.user_comment import IUserComment

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IUserComment)
    grok.require('zope2.View')
    grok.template('user_comment_view')
    grok.name('view')

