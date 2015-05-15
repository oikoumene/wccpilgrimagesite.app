from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.resources import IResources
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IResources)
    grok.require('zope2.View')
    grok.template('resources_view')
    grok.name('view')

    def resource_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
                sort_order='reverse',)
        videos = []
        sound = []
        documents = []
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.video:
                data= {'name': obj.name,
                        'email':obj.email,
                        'church': obj.church,
                        'message': obj.message,
                        'resource':obj.video,
                        'path':brain.getPath(),
                }
                videos.append(data)

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.sound:
                data= {'name': obj.name,
                        'email':obj.email,
                        'church': obj.church,
                        'message': obj.message,
                        'resource':obj.sound,
                        'path':brain.getPath(),
                }
                sound.append(data)


        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.document:
                data= {'name': obj.name,
                        'email':obj.email,
                        'church': obj.church,
                        'message': obj.message,
                        'resource':obj.document.filename,
                        'path':brain.getPath(),
                }
                documents.append(data)
        return {'videos': videos, 'sound': sound, 'documents': documents}

