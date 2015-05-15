from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps
from Products.CMFCore.utils import getToolByName


grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IPilgrimageSteps)
    grok.require('zope2.View')
    grok.template('pilgrimage_steps_view')
    grok.name('view')

    def comments_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.usercomment')[:3]
	return brains

    def resources_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        result = []
        brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
                sort_order='reverse',)
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.video:
                data= {'title': obj.title,
                        'name': obj.name,
                        'email':obj.email,
                        'church': obj.church,
                        'message': obj.message,
                        'resource':obj.video,
                        'type': "video",
                        'path':brain.getPath(),
                }
                result.append(data)
                break;

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.sound:
                data= {'title': obj.title,
                        'name': obj.name,
                        'email':obj.email,
                        'church': obj.church,
                        'message': obj.message,
                        'resource':obj.sound,
                        'type': "sound",
                        'path':brain.getPath(),
                }
                result.append(data)
                break;

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.document:
                data= {'title': obj.title,
                        'name': obj.name,
                        'email':obj.email,
                        'church': obj.church,
                        'message': obj.message,
                        'resource':obj.document.filename,
                        'type': "document",
                        'path':brain.getPath(),
                }
                result.append(data)
                break;


        return result


    def datetime_result(self, value=None):
        return value.strftime("%Y-%m-%d %H:%M")
