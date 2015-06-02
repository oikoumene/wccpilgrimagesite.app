from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_app import IPilgrimageApp
from Products.CMFCore.utils import getToolByName


import urlparse
from wccpilgrimagesite.app import MessageFactory as _
from zope.i18n import translate
from operator import itemgetter
from wccpilgrimagesite.app.content.video import IVideo
from wccpilgrimagesite.app.content.sound import ISound
from wccpilgrimagesite.app.content.static_document import IStaticDocument
import itertools

grok.templatedir('templates')

class resource_search(dexterity.DisplayForm):
    grok.context(IPilgrimageApp)
    grok.require('zope2.View')
    grok.template('resource_search')

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    #query results
    def contents (self):
        context = self.context
        request = self.request
        form = request.form
        results = []
        videos = []
        sounds = []
        documents = []
        pilgrimage_steps = ''
        resource_type = ''
        keyword = ''

        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps', review_state= 'published')
        for brain in brains:
            path = brain.getPath()

            if form:
                pilgrimage_steps = form['pilgrimage_steps']
                resource_type = form['resource_type']
                keyword = form['keyword']
            if pilgrimage_steps == 'all':
                if resource_type == 'all':
                    brains1 = catalog.unrestrictedSearchResults(path={'query':path, 'depth':2}, portal_type=['wccpilgrimagesite.app.video','wccpilgrimagesite.app.sound', 'wccpilgrimagesite.app.staticdocument'], review_state= 'published')
                    for brain1 in brains1:
                        obj = brain1._unrestrictedGetObject()
                        if keyword:
                            if keyword in brain1.Title or keyword in obj.description:
                                if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                    videos.append(self.video_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                    sounds.append(self.sound_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                    documents.append(self.document_result(brain1.UID))
                        else:
                            if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                videos.append(self.video_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                sounds.append(self.sound_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                documents.append(self.document_result(brain1.UID))

                else:
                    brains1 = catalog.unrestrictedSearchResults(path={'query':path, 'depth':2}, portal_type="wccpilgrimagesite.app."+resource_type, review_state= 'published')
                    
                    for brain1 in brains1:
                        obj = brain1._unrestrictedGetObject()
                        if keyword:
                            if keyword in brain1.Title or keyword in obj.description:
                                if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                    videos.append(self.video_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                    sounds.append(self.sound_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                    documents.append(self.document_result(brain1.UID))
                        else:
                            if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                videos.append(self.video_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                sounds.append(self.sound_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                documents.append(self.document_result(brain1.UID))



            if brain.UID == pilgrimage_steps:
                if resource_type == 'all':
                    brains1 = catalog.unrestrictedSearchResults(path={'query':path, 'depth':2}, portal_type=['wccpilgrimagesite.app.video','wccpilgrimagesite.app.sound','wccpilgrimagesite.app.staticdocument'], review_state= 'published')
                    
                    for brain1 in brains1:
                        obj = brain1._unrestrictedGetObject()
                        if keyword:
                            if keyword in brain1.Title or keyword in obj.description:
                                if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                    videos.append(self.video_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                    sounds.append(self.sound_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                    documents.append(self.document_result(brain1.UID))
                        else:
                            if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                videos.append(self.video_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                sounds.append(self.sound_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                documents.append(self.document_result(brain1.UID))

                else:
                    brains1 = catalog.unrestrictedSearchResults(path={'query':path, 'depth':2}, portal_type="wccpilgrimagesite.app."+resource_type, review_state= 'published')
                    
                    for brain1 in brains1:
                        obj = brain1._unrestrictedGetObject()
                        if keyword:
                            if keyword in brain1.Title or keyword in obj.description:
                                if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                    videos.append(self.video_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                    sounds.append(self.sound_result(brain1.UID))
                                if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                    documents.append(self.document_result(brain1.UID))
                        else:
                            if brain1.portal_type == 'wccpilgrimagesite.app.video':
                                videos.append(self.video_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.sound':
                                sounds.append(self.sound_result(brain1.UID))
                            if brain1.portal_type == 'wccpilgrimagesite.app.staticdocument':
                                documents.append(self.document_result(brain1.UID))

        return {'videos': videos, 'sounds':sounds, 'documents': documents}
    #pilgrimage steps

    def pilgrimage_steps(self):
        results = [{'value':'all', 'name':'All'}]
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps', review_state= 'published')
        for brain in brains:
            results.append({'value':brain.UID,
                            'name':brain.Title})
        return results

    #input form
    def searchedValue(self, val=None):
        request = self.request
        if request.form:
            return request.form[val]
        return  

    def video_result(self, uid = None):
        catalog = self.catalog
        context = self.context
        data = {}
        brains = catalog.unrestrictedSearchResults(object_provides=IVideo.__identifier__, UID= uid)
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            data = {'title': obj.title,
                        'description':obj.description,
                        'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}      
        return data 

    def sound_result(self, uid = None):
        catalog = self.catalog
        context = self.context
        data = {}
        brains = catalog.unrestrictedSearchResults(object_provides=ISound.__identifier__, UID= uid)
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            data = {'title': obj.title,
                        'description':obj.description,
                        'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}      
        return data 

    def document_result(self, uid = None):
        catalog = self.catalog
        context = self.context
        data = {}
        brains = catalog.unrestrictedSearchResults(object_provides=IStaticDocument.__identifier__, UID= uid)
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            data = {'title': obj.title,
                        'description':obj.description,
                        'file':obj.file,
                        'file_thumb': obj.file_thumb,
                        'path': brain.getPath(),
                        'uid': brain.UID,
                        'votes_count': obj.votes_count,
                        'created': brain.created,
                        'wcc_user':obj.wcc_user}      
        return data 

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
