from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.resources import IResources
from Products.CMFCore.utils import getToolByName
import urlparse
from wccpilgrimagesite.app import MessageFactory as _
from zope.i18n import translate
from operator import itemgetter
from wccpilgrimagesite.app.content.video import IVideo
from wccpilgrimagesite.app.content.sound import ISound
from wccpilgrimagesite.app.content.static_document import IStaticDocument
import itertools
import copy

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IResources)
    grok.require('zope2.View')
    grok.template('resources_view')
    grok.name('view')

    def videos_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        resources = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.video',sort_on='Date',
                sort_order='reverse',review_state= 'published')
        steps = catalog.unrestrictedSearchResults(object_provides=IVideo.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
        videos_resources = []
        videos_steps = []
        for brain in resources:
            obj = brain._unrestrictedGetObject()
            data_resources = {'title': obj.title,
                        'description':obj.description,
                        'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}
            videos_resources.append(data_resources)

        for brain in steps:
            obj = brain._unrestrictedGetObject()
            if obj.video_in_step:
                if context.aq_parent.UID() in obj.video_in_step:
                    data_steps = {'title': obj.title,
                        'description':obj.description,
                        'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}
                
                    videos_steps.append(data_steps)
        
        videos_final =copy.copy(videos_steps)
        for video in videos_resources:
            if video not in videos_steps:
                videos_final.append(video)
        if videos_final:
            videos_final.sort(key=lambda k: k['created'], reverse=True) 
        return videos_final



    # def sound_result(self):
    #     context = self.context
    #     catalog = getToolByName(context, 'portal_catalog')
    #     path = '/'.join(context.getPhysicalPath())
    #     brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.sound',sort_on='Date',
    #             sort_order='reverse',)
    #     sounds = []
      
    #     for brain in brains:
    #         obj = brain._unrestrictedGetObject()
            
    #         data= {'title': obj.title,
    #                     'description':obj.description,
    #                     'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
    #                     'sound_in_step': obj.sound_in_step,
    #                     'featured_sound_in_step':obj.featured_sound_in_step,
    #                     'uid': brain.UID,
    #                     'votes_count': obj.votes_count
    #             }
    #         sounds.append(data)
    #     return sounds

    def sound_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        resources = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.sound',sort_on='Date',
                sort_order='reverse',review_state= 'published')
        steps = catalog.unrestrictedSearchResults(object_provides=ISound.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
        sounds_resources = []
        sounds_steps = []
        for brain in resources:
            obj = brain._unrestrictedGetObject()
            data_resources = {'title': obj.title,
                        'description':obj.description,
                        'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}
            sounds_resources.append(data_resources)

        for brain in steps:
            obj = brain._unrestrictedGetObject()
            if obj.sound_in_step:
                if context.aq_parent.UID() in obj.sound_in_step:
                    data_steps = {'title': obj.title,
                        'description':obj.description,
                        'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}
                
                    sounds_steps.append(data_steps)
        
        sounds_final = copy.copy(sounds_steps)
        for sound in sounds_resources:
            if sound not in sounds_steps:
                sounds_final.append(sound)
        if sounds_final:
            sounds_final.sort(key=lambda k: k['created'], reverse=True) 
        return sounds_final

    # def document_result(self):
    #     context = self.context
    #     catalog = getToolByName(context, 'portal_catalog')
    #     path = '/'.join(context.getPhysicalPath())
    #     brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.staticdocument',sort_on='Date',
    #             sort_order='reverse',)
    #     docs = []
      
    #     for brain in brains:
    #         obj = brain._unrestrictedGetObject()
            
    #         data= {'title': obj.title,
    #                     'description':obj.description,
    #                     'file':obj.file,
    #                     'file_thumb': obj.file_thumb,
    #                     'doc_in_step':obj.doc_in_step,
    #                     'featured_doc_in_step':obj.featured_doc_in_step,
    #                     'path': brain.getURL(),
    #                     'uid': brain.UID,
    #                     'votes_count': obj.votes_count
    #             }
    #         docs.append(data)
    #     return docs

    def document_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        resources = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.staticdocument',sort_on='Date',
                sort_order='reverse',review_state= 'published')
        steps = catalog.unrestrictedSearchResults(object_provides=IStaticDocument.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
        docs_resources = []
        docs_steps = []
        for brain in resources:
            obj = brain._unrestrictedGetObject()
            data_resources= {'title': obj.title,
                        'description':obj.description,
                        'file':obj.file,
                        'file_thumb': obj.file_thumb,
                        'path': brain.getURL(),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user,
                        'app_type':obj.file.contentType

                }
            docs_resources.append(data_resources)

        for brain in steps:
            obj = brain._unrestrictedGetObject()
            if obj.doc_in_step:
                if context.aq_parent.UID() in obj.doc_in_step:
                    data_steps= {'title': obj.title,
                        'description':obj.description,
                        'file':obj.file,
                        'file_thumb': obj.file_thumb,
                        'path': brain.getURL(),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user,
                        'app_type':obj.file.contentType
                }
                
                    docs_steps.append(data_steps)
        docs_final = copy.copy(docs_steps)
        
        for doc in docs_resources:
            if doc not in docs_steps:
                docs_final.append(doc)
        if docs_final:
            docs_final.sort(key=lambda k: k['created'], reverse=True)    
        #return sorted(docs_final, key=itemgetter('created'), reverse=True)
        
        return docs_final

    def url_youtube_bg_img(self, url=None):
        return '//img.youtube.com/vi/{hash}/hqdefault.jpg'.format(hash=self._hash_from_url_youtube(url))

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
        return '//www.youtube.com/embed/{hash}'.format(hash=self._hash_from_url_youtube(url))
    
    def save_translation(self):
        return self.context.translate(_(u"Save"))
    
    def cancel_translation(self):
        return self.context.translate(_(u"Cancel"))


    def soundcloud_url_embedded(self, soundcloud = None):
        return 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{soundcloud}' \
               '&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=false&amp;' \
               'show_user=false&amp;show_reposts=false'.format(
            soundcloud=soundcloud
        )

    def soundcloud_url_frame(self, soundcloud = None):
        return 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{soundcloud}' \
               '&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;' \
               'show_reposts=false&amp;visual=true'.format(
            soundcloud=soundcloud
        )
            
    
    def see_more_button(self, resource_type=None):
        if resource_type == 'videos':
            return len(self.videos_result())
        
    def at_least_one_resource_msg(self):
        return _(u"At least one resource is required.")
    
    def no_name_provided(self):
        return _(u"No name provided.")
    
    def no_message_provided(self):
        return _(u"No message provided.")
