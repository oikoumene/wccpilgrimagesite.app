from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps
from Products.CMFCore.utils import getToolByName
import urlparse


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

    # def video_result(self):
    #     context = self.context
    #     catalog = getToolByName(context, 'portal_catalog')
    #     path = '/'.join(context.getPhysicalPath())
    #     result = []
    #     query = {}
    #     data = {}
    #     query['Subject'] = 'featured'
    #     brains = catalog.searchResults(query,path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
    #             sort_order='reverse', )
    #     if not brains:
    #         brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
    #             sort_order='reverse',)
    #     for brain in brains:
    #         obj = brain._unrestrictedGetObject()
    #         if obj.video:
    #             data= { 'name': obj.name,
    #                     'email':obj.email,
    #                     'church': obj.church,
    #                     'message': obj.message,
    #                     'resource':obj.video,
    #                     'path':brain.getPath(),
    #                     'tags': brain.Subject
    #                 }
    #             break;
    #     return data

    def video_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        result = []
        query = {}
        data = {}

        brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.video',sort_on='Date',
                sort_order='reverse',)

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if 'Featured' in str(obj.featured_resource): 
                data= { 'title': obj.title,
                        'description':obj.description,
                        'church':obj.church,
                        'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                        'featured_resource': obj.featured_resource,
                        }
                break;
        if bool(data) == False:
            for brain in brains:
                obj = brain._unrestrictedGetObject()
                data= { 'title': obj.title,
                            'description':obj.description,
                            'church':obj.church,
                            'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                            'featured_resource': obj.featured_resource,
                            }
                break;
              
        return data

    # def sound_result(self):
    #     context = self.context
    #     catalog = getToolByName(context, 'portal_catalog')
    #     path = '/'.join(context.getPhysicalPath())
    #     result = []
    #     query = {}
    #     data = {}
    #     query['Subject'] = 'featured'
    #     brains = catalog.searchResults(query,path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
    #             sort_order='reverse', )
    #     if not brains:
    #         brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
    #             sort_order='reverse',)
    #     for brain in brains:
    #         obj = brain._unrestrictedGetObject()
    #         if obj.sound:
    #             data= { 'name': obj.name,
    #                     'email':obj.email,
    #                     'church': obj.church,
    #                     'message': obj.message,
    #                     'resource':obj.video,
    #                     'path':brain.getPath(),
    #                     'tags': brain.Subject
    #                 }
    #             break;
    #     return data

    def sound_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        result = []
        query = {}
        data = {}

        brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.sound',sort_on='Date',
                sort_order='reverse',)

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if 'Featured' in str(obj.featured_resource): 
                data= { 'title': obj.title,
                        'description':obj.description,
                        'church':obj.church,
                        'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                        'featured_resource': obj.featured_resource,
                        }
                break;
        if bool(data) == False:
            for brain in brains:
                obj = brain._unrestrictedGetObject()
                data= { 'title': obj.title,
                            'description':obj.description,
                            'church':obj.church,
                            'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                            'featured_resource': obj.featured_resource,
                            }
                break;
              
        return data


    # def document_result(self):
    #     context = self.context
    #     catalog = getToolByName(context, 'portal_catalog')
    #     path = '/'.join(context.getPhysicalPath())
    #     result = []
    #     query = {}
    #     data = {}
    #     query['Subject'] = 'featured'
    #     brains = catalog.searchResults(query,path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
    #             sort_order='reverse', )
    #     if not brains:
    #         brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.resourceupload',sort_on='Date',
    #             sort_order='reverse',)
    #     for brain in brains:
    #         obj = brain._unrestrictedGetObject()
    #         if obj.document:
    #             data= { 'name': obj.name,
    #                     'email':obj.email,
    #                     'church': obj.church,
    #                     'message': obj.message,
    #                     'resource':obj.video,
    #                     'path':brain.getPath(),
    #                     'tags': brain.Subject
    #                 }
    #             break;
    #     return data

    def document_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        result = []
        query = {}
        data = {}

        brains = catalog.searchResults(path={'query':path, 'depth':3}, portal_type='wccpilgrimagesite.app.staticdocument',sort_on='Date',
                sort_order='reverse',)

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if 'Featured' in str(obj.featured_resource): 
                data= { 'title': obj.title,
                        'description':obj.description,
                        'church':obj.church,
                        'file': obj.file,
                        'featured_resource': obj.featured_resource,
                        'path': brain.getPath(),
                        }
                break;
        if bool(data) == False:
            for brain in brains:
                obj = brain._unrestrictedGetObject()
                data= { 'title': obj.title,
                            'description':obj.description,
                            'church':obj.church,
                            'file': obj.file,
                            'featured_resource': obj.featured_resource,
                            'path': brain.getPath(),
                            }
                break;
              
        return data


    def datetime_result(self, value=None):
        return value.strftime("%Y-%m-%d %H:%M")
    
    
    def resources_path(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.unrestrictedSearchResults(path={'query':'/'.join(self.context.getPhysicalPath()), 'depth':1}, portal_type='wccpilgrimagesite.app.resources')
        for brain in brains:
            return brain.getPath()
        return '#'

    def instagram_hashtags_joined(self, hashtag=None):
        if not hashtag or '@' in hashtag:
            return u''
        return u','.join(map(
            lambda x: x.strip(),
            hashtag.replace('#', '').split(',')
        ))

    def instagram_user_feed(self, hashtag=None):
        if not hashtag or '#' in hashtag:
            return u''
        return hashtag.replace('@', '').strip()

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

    def soundcloud_url_embedded(self, soundcloud = None):
        return 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{soundcloud}' \
               '&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=false&amp;' \
               'show_user=false&amp;show_reposts=false'.format(
            soundcloud=soundcloud
        )