import json

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#import plone.api
from Products.CMFCore.utils import getToolByName
from wccpilgrimagesite.app.content.video import IVideo
from wccpilgrimagesite.app.content.sound import ISound
from zope.component.hooks import getSite
from wccpilgrimagesite.app.content.static_document import IStaticDocument
import urlparse
import copy
from operator import itemgetter


#from wccpilgrimagesite.app import utils, content

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False
        

class ApiView(BrowserView):

    def _response(self, response={}, status_code=200, status_message=''):
        view_response = self.request.response
        view_response.setHeader('Content-type', 'application/json')
        view_response.setStatus(status_code, status_message)
        view_response.setBody(json.dumps(response), lock=True)

        return view_response


class ApiUpvoteView(ApiView):

    def __call__(self):
        id = self.request.form.get('id')
        if not id:
            return self._response(status_code=400)

        obj = plone.api.content.get(UID=id)
        if not obj:
            return self._response(status_code=400)

        obj.upvote1()

        return self._response()
    
class ResourceVideosPaginate(ApiView):
    
    def __call__(self):
        html = ''
        show_see_more = True
        if self.request:
            if self.request.form:
                form = self.request.form
                path = form.get('path')[:-1]
                step = form.get('step')
                parent_path = form.get('parent_aqparent_path')
                parent_UID = ''
                startPage = 0
                if is_number(step):
                    startPage = int(step)
                portal = getSite()
                catalog = getToolByName(portal, 'portal_catalog')
                resources = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.video',sort_on='Date',
                                                sort_order='reverse',review_state= 'published')
                steps = catalog.unrestrictedSearchResults(object_provides=IVideo.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
                
                parents = catalog.unrestrictedSearchResults(path={'query':parent_path, 'depth':0}, portal_type='wccpilgrimagesite.app.pilgrimagesteps')
                for prnt in parents:
                    parent_UID = prnt.UID
                
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
                        if parent_UID in obj.video_in_step:
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
                paginated_videos = []
                if len(videos_final) > 3:
                    videos_final.sort(key=lambda k: k['created'], reverse=True) 
                    paginated_videos = videos_final[startPage*3:(startPage*3)+3]
                
                for pv in paginated_videos:
                    html += "<li class='animated fadeInRight'>"
                    html += "<h3>"+pv['title']+"</h3>"
                    html += "<div>"
                    html += "<a class='video-links fancybox.iframe' href="+pv['url_youtube']+">"
                    html += "<img src="+self.url_youtube_bg_img(pv['url_youtube'])+"></a>"
                    html += "</div>"
                    html += "<ul class='no-bullet icons-box'>"
                    if pv['wcc_user']:
                        html += "<li class='user-icon wcc-user'>"
                        html += "<img src='++theme++wccpilgrimagesite.theme/images/wcc-user-icon.png' alt='' />"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    else:
                        html += "<li class='user-icon unknown-user'>"
                        html += "<i class='fa fa-user'></i>"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    html += "<li class='heart-icon'>"
                    html += "<a data-votable="+pv['uid']+"><i class='fa fa-heart'></i></a>"
                    html += "</li>"
                    html += "<li class='heart-count' data-votes-count="+pv['uid']+">"+str(pv['votes_count'])+"</li>"
                    html += "</ul>"
                    html += "<p>"+pv['description']+"</p>"
                    html += "</li>"
                
                if len(videos_final)-1 >= startPage*3 and len(videos_final)-1 <= (startPage*3)+2:
                    show_see_more = False
        return self._response(response={'html':html, 'show_see_more':show_see_more})
                    
                    
    def url_youtube_bg_img(self, url=None):
        return 'http://img.youtube.com/vi/{hash}/hqdefault.jpg'.format(hash=self._hash_from_url_youtube(url))
    
    def url_youtube_embedded(self, url=None):
        return 'http://www.youtube.com/embed/{hash}'.format(hash=self._hash_from_url_youtube(url))
    
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
    
    
class ResourceSoundsPaginate(ApiView):
    def __call__(self):
        html = ''
        show_see_more = True
        if self.request:
            if self.request.form:
                form = self.request.form
                if form.get('path').endswith('/'):
                    path = form.get('path')[:-1]
                else:
                    path = form.get('path')
                step = form.get('step')
                parent_path = form.get('parent_aqparent_path')
                parent_UID = ''
                startPage = 0
                if is_number(step):
                    startPage = int(step)
                portal = getSite()
                catalog = getToolByName(portal, 'portal_catalog')
                resources = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.sound',sort_on='Date',
                                                                sort_order='reverse',review_state= 'published')
                steps = catalog.unrestrictedSearchResults(object_provides=ISound.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
                
                
                parnts = catalog.unrestrictedSearchResults(path={'query':parent_path, 'depth':0}, portal_type='wccpilgrimagesite.app.pilgrimagesteps')
                
                for prnt in parnts:
                    parent_UID = prnt.UID
                
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
                        if parent_UID in obj.sound_in_step:
                            data_steps = {'title': obj.title,
                                'description':obj.description,
                                'soundcloud_id': self.soundcloud_url_embedded(obj.soundcloud_id),
                                'uid': brain.UID,
                                'votes_count': obj.votes_count,
                                'created': brain.created,
                                'wcc_user':obj.wcc_user}
                        
                            sounds_steps.append(data_steps)
                
                sounds_final =copy.copy(sounds_steps)
                for sound in sounds_resources:
                    if sound not in sounds_steps:
                        sounds_final.append(sound)
                
                paginated_sounds = []
                if len(sounds_final) > 3:
                    sounds_final.sort(key=lambda k: k['created'], reverse=True) 
                    paginated_sounds = sounds_final[startPage*3:(startPage*3)+3]
                
                for ps in paginated_sounds:
                    #html += "<li class='fadeInRight'>"
                    html += '<li>'
                    html += "<h3>"+ps['title']+"</h3>"
                    html += "<iframe src="+ps['soundcloud_id']+" width='100%' height='166' scrolling='no' frameborder='no'></iframe>"
                    html += "<ul class='no-bullet icons-box'>"
                    if ps['wcc_user']:
                        html += "<li class='user-icon wcc-user'>"
                        html += "<img src='++theme++wccpilgrimagesite.theme/images/wcc-user-icon.png' alt='' />"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    else:
                        html += "<li class='user-icon unknown-user'>"
                        html += "<i class='fa fa-user'></i>"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    html += "<li class='heart-icon'>"
                    html += "<a data-votable="+ps['uid']+"><i class='fa fa-heart'></i></a>"
                    html += "<li>"
                    html += "<li class='heart-count' data-votes-count="+ps['uid']+">"+str(ps['votes_count'])+"</li>"
                    html += "</ul>"
                    html += "<p>"+ps['description']+"</p>"
                    html += "</li>"
                if len(sounds_final)-1 >= startPage*3 and len(sounds_final)-1 <= (startPage*3)+2:
                    show_see_more = False
        return self._response(response={'html':html, 'show_see_more':show_see_more})
                
                
    
    def soundcloud_url_embedded(self, soundcloud = None):
        return 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{soundcloud}' \
               '&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=false&amp;' \
               'show_user=false&amp;show_reposts=false'.format(
            soundcloud=soundcloud
        )
            

class ResourceDocumentsPaginate(ApiView):
    def __call__(self):
        html = ''
        show_see_more = True
        if self.request:
            if self.request.form:
                form = self.request.form
                if form.get('path').endswith('/'):
                    path = form.get('path')[:-1]
                else:
                    path = form.get('path')
                step = form.get('step')
                parent_path = form.get('parent_aqparent_path')
                parent_UID = ''
                startPage = 0
                if is_number(step):
                    startPage = int(step)
                portal = getSite()
                catalog = getToolByName(portal, 'portal_catalog')
                resources = catalog.unrestrictedSearchResults(path={'query':path, 'depth':1}, portal_type='wccpilgrimagesite.app.staticdocument',sort_on='Date',
                                                sort_order='reverse',review_state= 'published')
                steps = catalog.unrestrictedSearchResults(object_provides=IStaticDocument.__identifier__,sort_on='Date',sort_order='reverse',review_state= 'published')
                
                parnts = catalog.unrestrictedSearchResults(path={'query':parent_path, 'depth':0}, portal_type='wccpilgrimagesite.app.pilgrimagesteps')
                
                for prnt in parnts:
                    parent_UID = prnt.UID
                docs_resources = []
                docs_steps = []
                for brain in resources:
                    obj = brain._unrestrictedGetObject()
                    data_resources= {'title': obj.title,
                                'description':obj.description,
                                'file':obj.file,
                                'file_thumb': obj.file_thumb,
                                'path': brain.getPath(),
                                'uid': brain.UID,
                                'votes_count': obj.votes_count,
                                'created': brain.created,
                                'wcc_user':obj.wcc_user
        
                        }
                    docs_resources.append(data_resources)
        
                for brain in steps:
                    obj = brain._unrestrictedGetObject()
                    if obj.doc_in_step:
                        if parent_UID in obj.doc_in_step:
                            data_steps= {'title': obj.title,
                                'description':obj.description,
                                'file':obj.file,
                                'file_thumb': obj.file_thumb,
                                'path': brain.getPath(),
                                'uid': brain.UID,
                                'votes_count': obj.votes_count,
                                'created': brain.created,
                                'wcc_user':obj.wcc_user
                        }
                        
                            docs_steps.append(data_steps)
        
                docs_final = copy.copy(docs_steps)
                for doc in docs_resources:
                    if doc not in docs_steps:
                        docs_final.append(doc)
                  
                paginated_docs = []
                if len(docs_final) > 3:
                    docs_final.sort(key=lambda k: k['created'], reverse=True) 
                    paginated_docs = docs_final[startPage*3:(startPage*3)+3]
                
                for pd in paginated_docs:
                    html += "<li class='animated fadeInRight'>"
                    html += "<h3>"+pd['title']+"</h3>"
                    html += "<a class='video-links fancybox.iframe' href="+pd['path']+"/@@images/file>"
                    if pd['file_thumb']:
                        html += "<img src="+pd['path']+"/@@display-file/file_thumb alt=''>"
                    else:
                        html += "<p class='fa fa-file-pdf-o' style='font-size: 150px;'></p> "
                    html += "</a>"
                    html += "<ul class='no-bullet icons-box'>"
                    if pd['wcc_user']:
                        html += "<li class='user-icon wcc-user'>"
                        html += "<img src='++theme++wccpilgrimagesite.theme/images/wcc-user-icon.png' alt='' />"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    else:
                        html += "<li class='user-icon unknown-user'>"
                        html += "<i class='fa fa-user'></i>"
                        html += "<span class='access'>User</span>"
                        html += "</li>"
                    html += "<li class='heart-icon'>"
                    html += "<a data-votable="+pd['uid']+"><i class='fa fa-heart'></i></a>"
                    html += "<li>"
                    html += "<li class='heart-count' data-votes-count="+pd['uid']+">"+str(pd['votes_count'])+"</li>"
                    html += "</ul>"
                    html += "<p>"+pd['description']+"</p>"
                    html += "</li>"
                if len(docs_final)-1 >= startPage*3 and len(docs_final)-1 <= (startPage*3)+2:
                    show_see_more = False
        return self._response(response={'html':html, 'show_see_more':show_see_more})
                    
                
                    

