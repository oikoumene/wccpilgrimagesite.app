from five import grok
from plone.directives import dexterity, form
from wccpilgrimagesite.app.content.pilgrimage_steps import IPilgrimageSteps
from Products.CMFCore.utils import getToolByName
import urlparse
from wccpilgrimagesite.app.content.video import IVideo
from wccpilgrimagesite.app.content.sound import ISound
from wccpilgrimagesite.app.content.static_document import IStaticDocument

from wccpilgrimagesite.app import MessageFactory as _
from zope.i18n import translate

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
        brains = catalog.searchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.usercomment',sort_on='Date',
                sort_order='reverse', review_state= 'published')[:3]
        return brains

    def video_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        steps = catalog.unrestrictedSearchResults(object_provides=IVideo.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
        data_steps = {}
        result = []
       

        for brain in steps:
            obj = brain._unrestrictedGetObject()
            if obj.featured_video_in_step:
                if context.UID() in obj.featured_video_in_step:
                    data_steps = { 'title': obj.title,
                            'description':obj.description,
                            # 'church':obj.church,
                            'url_youtube': self.url_youtube_embedded(obj.url_youtube),
                            'created': brain.created
                            }
                    break;
        if data_steps:
            result = data_steps

        return result

    def sound_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        steps = catalog.unrestrictedSearchResults(object_provides=ISound.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
        data_steps = {}
        result = []
       

        for brain in steps:
            obj = brain._unrestrictedGetObject()
            if obj.featured_sound_in_step:
                if context.UID() in obj.featured_sound_in_step:
                    data_steps = { 'title': obj.title,
                            'description':obj.description,
                            # 'church':obj.church,
                            'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                            'created': brain.created
                            }
                    break;
        if data_steps:
            result = data_steps

        return result

    def document_result(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        steps = catalog.unrestrictedSearchResults(object_provides=IStaticDocument.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
        data_steps = {}
        result = []
       

        for brain in steps:
            obj = brain._unrestrictedGetObject()
            if obj.featured_doc_in_step:
                if context.UID() in obj.featured_doc_in_step:
                    data_steps = { 'title': obj.title,
                            'description':obj.description,
                            # 'church':obj.church,
                            'file': obj.file,
                            'created': brain.created,
                            'path': brain.getURL(),
                            }
                    break;
        if data_steps:
            result = data_steps

        return result

    def datetime_result(self, value=None):
        return value.strftime("%Y-%m-%d %H:%M")
    
    
    def resources_path(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.unrestrictedSearchResults(path={'query':'/'.join(self.context.getPhysicalPath()), 'depth':1}, portal_type='wccpilgrimagesite.app.resources',review_state= 'published')
        for brain in brains:
            return brain.getURL()
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
            
    def save_translation(self):
        return self.context.translate(_(u"Save"))
    
    def cancel_translation(self):
        return self.context.translate(_(u"Cancel"))
    
    def pilgrimage_steps_position(self):
        context = self.context
        parent = context.aq_parent
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog.unrestrictedSearchResults(path={'query':'/'.join(parent.getPhysicalPath()), 'depth':1}, portal_type='wccpilgrimagesite.app.pilgrimagesteps')
        result = {}
        for brain in brains:
            result[parent.getObjectPosition(brain.id)+1] = brain.id
        
        return result
            
    
    def current_object_position(self):
        parent = self.context.aq_parent
        return  parent.getObjectPosition(self.context.id) + 1
    
    def max_position(self):
        if self.pilgrimage_steps_position():
            return max(self.pilgrimage_steps_position())
        return None
    
    def min_position(self):
        if self.pilgrimage_steps_position():
            return min(self.pilgrimage_steps_position())
        return None
    
    def next_content(self, pos=None):
        parent = self.context.aq_parent
        #path = '/'.join(parent.getPhysicalPath())
        path = parent.absolute_url()
        if pos:
            current_pos = self.current_object_position()
            positions = self.pilgrimage_steps_position()
            min_pos = self.min_position()
            max_pos = self.max_position()
            if current_pos >= min_pos and current_pos < max_pos:
                return path+'/'+positions[current_pos+1]
        return '#'
    
    def previous_content(self, pos=None):
        parent = self.context.aq_parent
        #path = '/'.join(parent.getPhysicalPath())
        path = parent.absolute_url()
        if pos:
            current_pos = self.current_object_position()
            positions = self.pilgrimage_steps_position()
            min_pos = self.min_position()
            max_pos = self.max_position()
            if current_pos <= max_pos and current_pos > min_pos:
                return path+'/'+positions[current_pos-1]
        return '#'
    
    
    
    
