from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.resources import IResources
from Products.CMFCore.utils import getToolByName
import urlparse
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


    def video_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.video',sort_on='Date',
                sort_order='reverse',)
        videos = []
      
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            
            data= {'title': obj.title,
                        'description':obj.description,
                        'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                        'video_in_step': obj.video_in_step,
                        'featured_video_in_step':obj.featured_video_in_step,
                        'featured_resource':obj.featured_resource,
                }
            videos.append(data)
        return videos

    def sound_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.sound',sort_on='Date',
                sort_order='reverse',)
        videos = []
      
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            
            data= {'title': obj.title,
                        'description':obj.description,
                        'soundcloud_id': obj.soundcloud_id,
                        'sound_in_step': obj.sound_in_step,
                        'featured_sound_in_step':obj.featured_sound_in_step,
                        'featured_resource':obj.featured_resource,
                }
            videos.append(data)
        return videos

    def document_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.staticdocument',sort_on='Date',
                sort_order='reverse',)
        videos = []
      
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            
            data= {'title': obj.title,
                        'description':obj.description,
                        'file': obj.file,
                        'file_thumb': obj.file_thumb,
                        'doc_in_step':obj.doc_in_step,
                        'featured_doc_in_step':obj.featured_doc_in_step,
                        'featured_resource':obj.featured_resource,
                }
            videos.append(data)
        return videos

    def url_youtube_bg_img(self, url=None):
        return 'http://img.youtube.com/vi/{hash}/hqdefault.jpg'.format(hash=self._hash_from_url_youtube(url))

    def _hash_from_url_youtube(self, url=None):
        # Reference: http://stackoverflow.com/a/7936523/545435

        query = urlparse.urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urlparse.parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        return ''


    def url_youtube_embedded(self, url=None):
        return 'http://www.youtube.com/embed/{hash}'.format(hash=self._hash_from_url_youtube(url))

